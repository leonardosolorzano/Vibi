"""
Esquemas Pydantic para reserva.

Práctica aplicada: Complex Validation
- Validación de fechas (check-out > check-in)
- Validación de cantidad de huéspedes
- Respuestas anidadas con detalles completos
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    """Campos base de la reserva."""

    property_id: int = Field(..., gt=0, description="ID de la propiedad")
    check_in_date: datetime = Field(..., description="Fecha de entrada")
    check_out_date: datetime = Field(..., description="Fecha de salida")
    number_of_guests: int = Field(..., ge=1, description="Número de huéspedes")
    notes: Optional[str] = Field(None, max_length=500, description="Notas adicionales")

    @field_validator("check_out_date")
    @classmethod
    def check_out_after_check_in(cls, v: datetime, info):
        """Validar que la fecha de salida sea posterior a la de entrada."""
        if "check_in_date" in info.data and v <= info.data["check_in_date"]:
            raise ValueError("check_out_date debe ser posterior a check_in_date")
        return v


class BookingCreate(BookingBase):
    """Schema para crear una reserva."""

    pass


class BookingUpdate(BaseModel):
    """Schema para actualizar una reserva."""

    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    number_of_guests: Optional[int] = Field(None, ge=1)
    notes: Optional[str] = Field(None, max_length=500)
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    """Schema de respuesta de la reserva."""

    id: int
    guest_id: int
    total_price: float
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingDetailResponse(BookingResponse):
    """Schema de respuesta detallada con información de propiedad e huésped."""

    property: Optional["PropertyResponseBasic"] = None
    guest: Optional["UserResponseBasic"] = None

    class Config:
        from_attributes = True


# Imports para referencias cruzadas
from app.schemas.property import PropertyResponse as PropertyResponseBasic
from app.schemas.user import UserResponse as UserResponseBasic
