"""
Servicio de propiedad con lógica específica.

Práctica aplicada: Business Logic Separation
- Búsqueda avanzada por criterios
- Filtrado por ciudad, tipo, precio
- Paginación eficiente
"""

from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property, PropertyType
from app.services.base import BaseService


class PropertyService(BaseService[Property]):
    """Servicio para operaciones con propiedades."""

    def __init__(self):
        """Inicializa el servicio de propiedad."""
        super().__init__(Property)

    async def get_by_owner_id(
        self, session: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100
    ) -> list[Property]:
        """
        Obtiene propiedades de un propietario.

        Args:
            session: Sesión de BD
            owner_id: ID del propietario
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de propiedades
        """
        query = (
            select(self.model)
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def search(
        self,
        session: AsyncSession,
        city: Optional[str] = None,
        property_type: Optional[PropertyType] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_guests: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Property]:
        """
        Busca propiedades con múltiples criterios.

        Args:
            session: Sesión de BD
            city: Filtrar por ciudad
            property_type: Filtrar por tipo
            min_price: Precio mínimo por noche
            max_price: Precio máximo por noche
            min_guests: Cantidad mínima de huéspedes soportados
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de propiedades encontradas
        """
        conditions = [self.model.is_active == True]

        if city:
            conditions.append(self.model.city.ilike(f"%{city}%"))
        if property_type:
            conditions.append(self.model.property_type == property_type)
        if min_price is not None:
            conditions.append(self.model.price_per_night >= min_price)
        if max_price is not None:
            conditions.append(self.model.price_per_night <= max_price)
        if min_guests is not None:
            conditions.append(self.model.max_guests >= min_guests)

        query = select(self.model).where(and_(*conditions)).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_active_properties(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Property]:
        """
        Obtiene todas las propiedades activas.

        Args:
            session: Sesión de BD
            skip: Registros a saltar
            limit: Máximo de registros

        Returns:
            Lista de propiedades activas
        """
        query = (
            select(self.model)
            .where(self.model.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all()


# Instancia singleton del servicio
property_service = PropertyService()
