"""
Modelo de Usuario.

Práctica aplicada: Entity Modeling
- Uso de tipos de datos SQL adecuados
- Constraints para integridad de datos
- Relaciones declarativas
- Timestamps para auditoría
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """
    Modelo de usuario en la aplicación.

    Attributes:
        id: Identificador único
        email: Email único del usuario
        full_name: Nombre completo
        password_hash: Hash de la contraseña
        phone: Teléfono de contacto
        is_active: Si el usuario está activo
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    properties = relationship("Property", back_populates="owner")
    bookings = relationship("Booking", back_populates="guest")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
