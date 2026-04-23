"""
Esquemas Pydantic para usuario.

Práctica aplicada: Request/Response Validation
- Separación de esquemas para entrada y salida
- Validación automática con Pydantic
- Ocultamiento de campos sensibles en respuestas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Campos base del usuario."""

    email: EmailStr = Field(..., description="Email único del usuario")
    full_name: str = Field(..., min_length=1, max_length=255, description="Nombre completo")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")


class UserCreate(UserBase):
    """Schema para crear un usuario."""

    password: str = Field(..., min_length=8, max_length=255, description="Contraseña")


class UserUpdate(BaseModel):
    """Schema para actualizar un usuario."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    password: Optional[str] = Field(None, min_length=8, max_length=255)


class UserResponse(UserBase):
    """Schema de respuesta del usuario (sin información sensible)."""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
