"""
Servicio de reserva con lógica específica.

Práctica aplicada: Complex Business Rules
- Cálculo de precio total
- Validación de disponibilidad
- Filtrado por estado y fechas
- Prevención de overlapping
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.services.base import BaseService


class BookingService(BaseService[Booking]):
    """Servicio para operaciones con reservas."""

    def __init__(self):
        """Inicializa el servicio de reserva."""
        super().__init__(Booking)

    async def get_by_guest_id(
        self, session: AsyncSession, guest_id: int, skip: int = 0, limit: int = 100
    ) -> list[Booking]:
        """
        Obtiene reservas de un huésped.

        Args:
            session: Sesión de BD
            guest_id: ID del huésped
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de reservas
        """
        query = (
            select(self.model)
            .where(self.model.guest_id == guest_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_property_id(
        self, session: AsyncSession, property_id: int, skip: int = 0, limit: int = 100
    ) -> list[Booking]:
        """
        Obtiene reservas de una propiedad.

        Args:
            session: Sesión de BD
            property_id: ID de la propiedad
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de reservas
        """
        query = (
            select(self.model)
            .where(self.model.property_id == property_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def check_availability(
        self,
        session: AsyncSession,
        property_id: int,
        check_in: datetime,
        check_out: datetime,
        exclude_booking_id: Optional[int] = None,
    ) -> bool:
        """
        Verifica si una propiedad está disponible en las fechas indicadas.

        Una propiedad NO está disponible si hay una reserva confirmada
        que se superpone con las fechas solicitadas.

        Args:
            session: Sesión de BD
            property_id: ID de la propiedad
            check_in: Fecha de entrada deseada
            check_out: Fecha de salida deseada
            exclude_booking_id: ID de reserva a ignorar (para updates)

        Returns:
            True si está disponible, False en caso contrario
        """
        conditions = [
            self.model.property_id == property_id,
            self.model.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING]),
            # Valida que NO haya solapamiento de fechas
            self.model.check_in_date < check_out,
            self.model.check_out_date > check_in,
        ]

        if exclude_booking_id:
            conditions.append(self.model.id != exclude_booking_id)

        query = select(self.model).where(and_(*conditions))
        result = await session.execute(query)
        return result.scalars().first() is None

    async def calculate_total_price(
        self, session: AsyncSession, property_id: int, check_in: datetime, check_out: datetime
    ) -> float:
        """
        Calcula el precio total de una reserva.

        Args:
            session: Sesión de BD
            property_id: ID de la propiedad
            check_in: Fecha de entrada
            check_out: Fecha de salida

        Returns:
            Precio total (price_per_night * número de noches)
        """
        from app.services.property import property_service

        property_obj = await property_service.get_by_id(session, property_id)
        if not property_obj:
            return 0.0

        nights = (check_out - check_in).days
        return property_obj.price_per_night * nights

    async def get_by_status(
        self,
        session: AsyncSession,
        status: BookingStatus,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Booking]:
        """
        Obtiene reservas filtradas por estado.

        Args:
            session: Sesión de BD
            status: Estado de la reserva
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de reservas
        """
        query = (
            select(self.model)
            .where(self.model.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_upcoming_bookings(
        self, session: AsyncSession, property_id: int
    ) -> list[Booking]:
        """
        Obtiene reservas próximas (confirmadas y posteriores a hoy).

        Args:
            session: Sesión de BD
            property_id: ID de la propiedad

        Returns:
            Lista de reservas próximas ordenadas por fecha
        """
        now = datetime.utcnow()
        query = (
            select(self.model)
            .where(
                and_(
                    self.model.property_id == property_id,
                    self.model.status == BookingStatus.CONFIRMED,
                    self.model.check_in_date >= now,
                )
            )
            .order_by(self.model.check_in_date)
        )
        result = await session.execute(query)
        return result.scalars().all()


# Instancia singleton del servicio
booking_service = BookingService()
