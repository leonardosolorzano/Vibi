"""
Esquemas Pydantic para propiedad.

Práctica aplicada: Detailed Validation
- Validación de rangos (bedrooms, bathrooms, guests)
- Enumeración para tipos de propiedad
- Respuestas anidadas con información del propietario
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.property import PropertyType


class PropertyBase(BaseModel):
    """Campos base de la propiedad."""

    title: str = Field(..., min_length=1, max_length=255, description="Título de la propiedad")
    description: str = Field(..., min_length=10, description="Descripción detallada")
    property_type: PropertyType = Field(..., description="Tipo de propiedad")
    price_per_night: float = Field(..., gt=0, description="Precio por noche en USD")
    city: str = Field(..., min_length=1, max_length=100, description="Ciudad")
    address: str = Field(..., min_length=1, max_length=255, description="Dirección completa")
    max_guests: int = Field(..., ge=1, le=100, description="Número máximo de huéspedes")
    bedrooms: int = Field(..., ge=1, le=20, description="Cantidad de habitaciones")
    bathrooms: int = Field(..., ge=1, le=20, description="Cantidad de baños")


class PropertyCreate(PropertyBase):
    """Schema para crear una propiedad."""

    pass


class PropertyUpdate(BaseModel):
    """Schema para actualizar una propiedad."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=10)
    property_type: Optional[PropertyType] = None
    price_per_night: Optional[float] = Field(None, gt=0)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    max_guests: Optional[int] = Field(None, ge=1, le=100)
    bedrooms: Optional[int] = Field(None, ge=1, le=20)
    bathrooms: Optional[int] = Field(None, ge=1, le=20)
    is_active: Optional[bool] = None


class PropertyResponse(PropertyBase):
    """Schema de respuesta de la propiedad."""

    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PropertyDetailResponse(PropertyResponse):
    """Schema de respuesta detallada con información del propietario."""

    owner: Optional["UserResponseBasic"] = None

    class Config:
        from_attributes = True


from app.schemas.user import UserResponse as UserResponseBasic
