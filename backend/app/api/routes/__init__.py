"""Rutas de la API."""

from app.api.routes.bookings import router as bookings_router
from app.api.routes.properties import router as properties_router
from app.api.routes.users import router as users_router

__all__ = [
    "users_router",
    "properties_router",
    "bookings_router",
]
