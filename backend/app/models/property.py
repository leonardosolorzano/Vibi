"""
Modelo de Propiedad.

Práctica aplicada: Domain Modeling
- Enumeración para tipos de propiedades
- Relaciones con otros modelos
- Validación a nivel de BD
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class PropertyType(str, Enum):
    """Tipos de propiedades disponibles."""

    APARTMENT = "apartment"
    HOUSE = "house"
    VILLA = "villa"
    CABIN = "cabin"
    LOFT = "loft"


class Property(Base):
    """
    Modelo de propiedad/alojamiento.

    Attributes:
        id: Identificador único
        title: Título de la propiedad
        description: Descripción detallada
        property_type: Tipo de propiedad
        price_per_night: Precio por noche
        city: Ciudad donde está ubicada
        address: Dirección completa
        max_guests: Número máximo de huéspedes
        bedrooms: Cantidad de habitaciones
        bathrooms: Cantidad de baños
        owner_id: ID del propietario
        is_active: Si la propiedad está activa
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    property_type = Column(String(50), nullable=False)  # apartment, house, villa, etc
    price_per_night = Column(Float, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    max_guests = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="properties")
    bookings = relationship("Booking", back_populates="property", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Property(id={self.id}, title={self.title}, city={self.city})>"
