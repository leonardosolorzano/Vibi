"""API v1 del backend."""

from app.api.routes import auth_router, bookings_router, properties_router, users_router

__all__ = ["auth_router", "users_router", "properties_router", "bookings_router"]
