"""
Rutas de reservas.

Práctica aplicada: Complex Business Logic in Routes
- Validación de disponibilidad
- Cálculo automático de precios
- Gestión de estados
- Manejo de errores específicos del dominio
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models import Booking, BookingStatus
from app.schemas import BookingCreate, BookingDetailResponse, BookingResponse, BookingUpdate
from app.services import booking_service, property_service

router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"],
    responses={404: {"description": "Reserva no encontrada"}},
)


@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reserva",
)
async def create_booking(
    booking_in: BookingCreate,
    guest_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> Booking:
    """
    Crea una nueva reserva.

    Validaciones:
    - La propiedad debe existir
    - Debe haber disponibilidad en las fechas
    - El número de huéspedes debe ser válido

    Args:
        booking_in: Datos de la reserva
        guest_id: ID del huésped
        session: Sesión de BD inyectada

    Returns:
        Reserva creada

    Raises:
        HTTPException 404: Propiedad no encontrada
        HTTPException 400: Propiedad no disponible o datos inválidos
    """
    # Validar que la propiedad exista
    property_obj = await property_service.get_by_id(session, booking_in.property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Propiedad con ID {booking_in.property_id} no encontrada",
        )

    # Validar que el número de huéspedes no exceda la capacidad
    if booking_in.number_of_guests > property_obj.max_guests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La propiedad soporta máximo {property_obj.max_guests} huéspedes",
        )

    # Verificar disponibilidad
    is_available = await booking_service.check_availability(
        session,
        booking_in.property_id,
        booking_in.check_in_date,
        booking_in.check_out_date,
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La propiedad no está disponible en las fechas seleccionadas",
        )

    # Calcular precio total
    total_price = await booking_service.calculate_total_price(
        session,
        booking_in.property_id,
        booking_in.check_in_date,
        booking_in.check_out_date,
    )

    # Crear reserva
    booking_data = booking_in.model_dump()
    booking_data["guest_id"] = guest_id
    booking_data["total_price"] = total_price
    booking_data["status"] = BookingStatus.PENDING

    return await booking_service.create(session, booking_data)


@router.get(
    "",
    response_model=List[BookingResponse],
    summary="Listar reservas",
)
async def list_bookings(
    property_id: Optional[int] = None,
    guest_id: Optional[int] = None,
    status: Optional[BookingStatus] = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
) -> List[Booking]:
    """
    Obtiene lista de reservas con filtros opcionales.

    Args:
        property_id: Filtrar por propiedad
        guest_id: Filtrar por huésped
        status: Filtrar por estado
        skip: Registros a saltar
        limit: Máximo de registros
        session: Sesión de BD inyectada

    Returns:
        Lista de reservas
    """
    if property_id:
        return await booking_service.get_by_property_id(session, property_id, skip=skip, limit=limit)

    if guest_id:
        return await booking_service.get_by_guest_id(session, guest_id, skip=skip, limit=limit)

    if status:
        return await booking_service.get_by_status(session, status, skip=skip, limit=limit)

    return await booking_service.get_all(session, skip=skip, limit=limit)


@router.get(
    "/{booking_id}",
    response_model=BookingDetailResponse,
    summary="Obtener detalles de una reserva",
)
async def get_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Booking:
    """
    Obtiene los detalles completos de una reserva.

    Args:
        booking_id: ID de la reserva
        session: Sesión de BD inyectada

    Returns:
        Detalles de la reserva

    Raises:
        HTTPException 404: Reserva no encontrada
    """
    booking = await booking_service.get_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {booking_id} no encontrada",
        )
    return booking


@router.put(
    "/{booking_id}",
    response_model=BookingResponse,
    summary="Actualizar una reserva",
)
async def update_booking(
    booking_id: int,
    booking_in: BookingUpdate,
    guest_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> Booking:
    """
    Actualiza los datos de una reserva.

    Si se modifican fechas, se revalida la disponibilidad y recalcula el precio.

    Args:
        booking_id: ID de la reserva
        booking_in: Nuevos datos
        guest_id: ID del huésped (validación de ownership)
        session: Sesión de BD inyectada

    Returns:
        Reserva actualizada

    Raises:
        HTTPException 404: Reserva no encontrada
        HTTPException 403: No autorizado
        HTTPException 400: Datos inválidos o no disponible
    """
    booking = await booking_service.get_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {booking_id} no encontrada",
        )

    # Validar ownership
    if booking.guest_id != guest_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar esta reserva",
        )

    # Si se cambian las fechas, revalidar disponibilidad
    if booking_in.check_in_date or booking_in.check_out_date:
        check_in = booking_in.check_in_date or booking.check_in_date
        check_out = booking_in.check_out_date or booking.check_out_date

        is_available = await booking_service.check_availability(
            session, booking.property_id, check_in, check_out, exclude_booking_id=booking_id
        )
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La propiedad no está disponible en las nuevas fechas",
            )

        # Recalcular precio si cambian las fechas
        total_price = await booking_service.calculate_total_price(
            session, booking.property_id, check_in, check_out
        )
        booking_in.total_price = total_price  # type: ignore

    update_data = booking_in.model_dump(exclude_unset=True)
    return await booking_service.update(session, booking, update_data)


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancelar una reserva",
)
async def cancel_booking(
    booking_id: int,
    guest_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Cancela una reserva (cambia estado a CANCELLED).

    Args:
        booking_id: ID de la reserva
        guest_id: ID del huésped (validación de ownership)
        session: Sesión de BD inyectada

    Raises:
        HTTPException 404: Reserva no encontrada
        HTTPException 403: No autorizado
    """
    booking = await booking_service.get_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {booking_id} no encontrada",
        )

    # Validar ownership
    if booking.guest_id != guest_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para cancelar esta reserva",
        )

    # Cambiar estado a cancelado
    await booking_service.update(session, booking, {"status": BookingStatus.CANCELLED})


@router.patch(
    "/{booking_id}/confirm",
    response_model=BookingResponse,
    summary="Confirmar una reserva",
)
async def confirm_booking(
    booking_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Booking:
    """
    Confirma una reserva pendiente.

    Nota: En producción, esto requeriría validación de pago.

    Args:
        booking_id: ID de la reserva
        session: Sesión de BD inyectada

    Returns:
        Reserva confirmada

    Raises:
        HTTPException 404: Reserva no encontrada
    """
    booking = await booking_service.get_by_id(session, booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva con ID {booking_id} no encontrada",
        )

    return await booking_service.update(session, booking, {"status": BookingStatus.CONFIRMED})


@router.get(
    "/property/{property_id}/availability",
    summary="Obtener calendario de disponibilidad",
)
async def get_property_availability(
    property_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    """
    Obtiene las próximas reservas confirmadas de una propiedad.

    Útil para mostrar disponibilidad en calendario.

    Args:
        property_id: ID de la propiedad
        session: Sesión de BD inyectada

    Returns:
        Diccionario con las próximas reservas

    Raises:
        HTTPException 404: Propiedad no encontrada
    """
    property_obj = await property_service.get_by_id(session, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Propiedad con ID {property_id} no encontrada",
        )

    bookings = await booking_service.get_upcoming_bookings(session, property_id)

    return {
        "property_id": property_id,
        "reserved_dates": [
            {
                "check_in": booking.check_in_date.isoformat(),
                "check_out": booking.check_out_date.isoformat(),
            }
            for booking in bookings
        ],
    }
