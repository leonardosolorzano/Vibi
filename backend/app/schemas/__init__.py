"""Esquemas Pydantic para validación."""

from app.schemas.booking import (
    BookingCreate,
    BookingDetailResponse,
    BookingResponse,
    BookingUpdate,
)
from app.schemas.property import (
    PropertyCreate,
    PropertyDetailResponse,
    PropertyResponse,
    PropertyUpdate,
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate

__all__ = [
    # User schemas
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    # Property schemas
    "PropertyCreate",
    "PropertyResponse",
    "PropertyDetailResponse",
    "PropertyUpdate",
    # Booking schemas
    "BookingCreate",
    "BookingResponse",
    "BookingDetailResponse",
    "BookingUpdate",
]
