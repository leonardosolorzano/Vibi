"""
Rutas de propiedades.

Práctica aplicada: Advanced Filtering & Search
- Búsqueda con múltiples criterios
- Respuestas detalladas con relaciones
- Validación de ownership
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models import Property, PropertyType
from app.schemas import PropertyCreate, PropertyDetailResponse, PropertyResponse, PropertyUpdate
from app.services import property_service

router = APIRouter(
    prefix="/api/v1/properties",
    tags=["Properties"],
    responses={404: {"description": "Propiedad no encontrada"}},
)


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva propiedad",
)
async def create_property(
    property_in: PropertyCreate,
    owner_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> Property:
    """
    Crea una nueva propiedad.

    Args:
        property_in: Datos de la propiedad
        owner_id: ID del propietario
        session: Sesión de BD inyectada

    Returns:
        Propiedad creada

    Raises:
        HTTPException 400: Datos inválidos
    """
    property_data = property_in.model_dump()
    property_data["owner_id"] = owner_id

    return await property_service.create(session, property_data)


@router.get(
    "",
    response_model=List[PropertyResponse],
    summary="Listar propiedades",
)
async def list_properties(
    city: Optional[str] = None,
    property_type: Optional[PropertyType] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_guests: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
) -> List[Property]:
    """
    Obtiene lista de propiedades con búsqueda avanzada.

    Args:
        city: Filtrar por ciudad
        property_type: Filtrar por tipo (apartment, house, villa, etc)
        min_price: Precio mínimo por noche
        max_price: Precio máximo por noche
        min_guests: Huéspedes mínimos soportados
        skip: Registros a saltar
        limit: Máximo de registros
        session: Sesión de BD inyectada

    Returns:
        Lista de propiedades
    """
    return await property_service.search(
        session,
        city=city,
        property_type=property_type,
        min_price=min_price,
        max_price=max_price,
        min_guests=min_guests,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{property_id}",
    response_model=PropertyDetailResponse,
    summary="Obtener detalles de una propiedad",
)
async def get_property(
    property_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Property:
    """
    Obtiene los detalles completos de una propiedad.

    Args:
        property_id: ID de la propiedad
        session: Sesión de BD inyectada

    Returns:
        Detalles de la propiedad

    Raises:
        HTTPException 404: Propiedad no encontrada
    """
    property_obj = await property_service.get_by_id(session, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Propiedad con ID {property_id} no encontrada",
        )
    return property_obj


@router.put(
    "/{property_id}",
    response_model=PropertyResponse,
    summary="Actualizar una propiedad",
)
async def update_property(
    property_id: int,
    property_in: PropertyUpdate,
    owner_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> Property:
    """
    Actualiza los datos de una propiedad.

    Args:
        property_id: ID de la propiedad
        property_in: Nuevos datos
        owner_id: ID del propietario (validación de ownership)
        session: Sesión de BD inyectada

    Returns:
        Propiedad actualizada

    Raises:
        HTTPException 404: Propiedad no encontrada
        HTTPException 403: No autorizado
    """
    property_obj = await property_service.get_by_id(session, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Propiedad con ID {property_id} no encontrada",
        )

    # Validar ownership
    if property_obj.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar esta propiedad",
        )

    update_data = property_in.model_dump(exclude_unset=True)
    return await property_service.update(session, property_obj, update_data)


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una propiedad",
)
async def delete_property(
    property_id: int,
    owner_id: int,  # En producción: obtener del token autenticado
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Elimina una propiedad.

    Args:
        property_id: ID de la propiedad
        owner_id: ID del propietario (validación de ownership)
        session: Sesión de BD inyectada

    Raises:
        HTTPException 404: Propiedad no encontrada
        HTTPException 403: No autorizado
    """
    property_obj = await property_service.get_by_id(session, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Propiedad con ID {property_id} no encontrada",
        )

    # Validar ownership
    if property_obj.owner_id != owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para eliminar esta propiedad",
        )

    await property_service.delete(session, property_id)


@router.get(
    "/owner/{owner_id}/properties",
    response_model=List[PropertyResponse],
    summary="Listar propiedades de un propietario",
)
async def get_owner_properties(
    owner_id: int,
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
) -> List[Property]:
    """
    Obtiene todas las propiedades de un propietario.

    Args:
        owner_id: ID del propietario
        skip: Registros a saltar
        limit: Máximo de registros
        session: Sesión de BD inyectada

    Returns:
        Lista de propiedades del propietario
    """
    return await property_service.get_by_owner_id(session, owner_id, skip=skip, limit=limit)
