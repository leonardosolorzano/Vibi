"""
Servicio base con operaciones CRUD comunes.

Práctica aplicada: Repository Pattern
- Abstracción de operaciones de BD
- Métodos genéricos reutilizables
- Type hints para mayor seguridad
"""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Servicio base genérico con operaciones CRUD.

    Parámetros genéricos:
        T: Tipo de modelo de BD
    """

    def __init__(self, model: Type[T]):
        """
        Inicializa el servicio.

        Args:
            model: Clase del modelo SQLAlchemy
        """
        self.model = model

    async def create(self, session: AsyncSession, obj_in: dict) -> T:
        """
        Crea un nuevo registro.

        Args:
            session: Sesión de BD
            obj_in: Diccionario con datos

        Returns:
            Instancia creada
        """
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def get_by_id(self, session: AsyncSession, id: int) -> Optional[T]:
        """
        Obtiene un registro por ID.

        Args:
            session: Sesión de BD
            id: ID del registro

        Returns:
            Registro encontrado o None
        """
        return await session.get(self.model, id)

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[T]:
        """
        Obtiene todos los registros con paginación.

        Args:
            session: Sesión de BD
            skip: Registros a saltar
            limit: Máximo de registros a retornar

        Returns:
            Lista de registros
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def update(self, session: AsyncSession, db_obj: T, obj_in: dict) -> T:
        """
        Actualiza un registro.

        Args:
            session: Sesión de BD
            db_obj: Objeto a actualizar
            obj_in: Diccionario con nuevos datos

        Returns:
            Objeto actualizado
        """
        for key, value in obj_in.items():
            if value is not None:
                setattr(db_obj, key, value)
        session.add(db_obj)
        await session.flush()
        return db_obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """
        Elimina un registro.

        Args:
            session: Sesión de BD
            id: ID del registro a eliminar

        Returns:
            True si se eliminó, False si no existe
        """
        obj = await self.get_by_id(session, id)
        if obj:
            await session.delete(obj)
            await session.flush()
            return True
        return False
