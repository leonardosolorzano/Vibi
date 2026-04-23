"""
Servicio de usuario con lógica específica.

Práctica aplicada: Domain Logic Encapsulation
- Hashing de contraseña
- Búsqueda por email
- Métodos específicos del dominio
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService[User]):
    """Servicio para operaciones con usuarios."""

    def __init__(self):
        """Inicializa el servicio de usuario."""
        super().__init__(User)

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """
        Obtiene un usuario por email.

        Args:
            session: Sesión de BD
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_active_users(self, session: AsyncSession) -> list[User]:
        """
        Obtiene todos los usuarios activos.

        Args:
            session: Sesión de BD

        Returns:
            Lista de usuarios activos
        """
        query = select(self.model).where(self.model.is_active == True)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash de la contraseña.

        Nota: En producción, usar bcrypt u otro algoritmo seguro.

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña
        """
        # TODO: Implementar hashing seguro con bcrypt
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash.

        Args:
            plain_password: Contraseña en texto plano
            hashed_password: Hash almacenado

        Returns:
            True si coinciden, False en caso contrario
        """
        # TODO: Implementar verificación segura con bcrypt
        return UserService.hash_password(plain_password) == hashed_password


# Instancia singleton del servicio
user_service = UserService()
