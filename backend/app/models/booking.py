"""
Modelo de Reserva.

Práctica aplicada: State Management
- Enumeración para estados de reserva
- Validación de integridad referencial
- Auditoría con timestamps
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.core.database import Base
from sqlalchemy.orm import relationship


class BookingStatus(str, Enum):
    """Estados posibles de una reserva."""

    PENDING = "pending"  # Pendiente de pago
    CONFIRMED = "confirmed"  # Confirmada
    CANCELLED = "cancelled"  # Cancelada
    COMPLETED = "completed"  # Completada


class Booking(Base):
    """
    Modelo de reserva de alojamiento.

    Attributes:
        id: Identificador único
        property_id: ID de la propiedad reservada
        guest_id: ID del huésped
        check_in_date: Fecha de entrada
        check_out_date: Fecha de salida
        number_of_guests: Cantidad de huéspedes
        total_price: Precio total de la reserva
        status: Estado de la reserva
        notes: Notas adicionales
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False, index=True)
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    check_in_date = Column(DateTime, nullable=False, index=True)
    check_out_date = Column(DateTime, nullable=False, index=True)
    number_of_guests = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default=BookingStatus.PENDING, nullable=False, index=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    property = relationship("Property", back_populates="bookings")
    guest = relationship("User", back_populates="bookings")

    def __repr__(self) -> str:
        return f"<Booking(id={self.id}, property_id={self.property_id}, status={self.status})>"
