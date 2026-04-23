"""
Configuración de tests con pytest.

Proporciona fixtures compartidas para todos los tests.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.main import app


@pytest.fixture
async def test_db_session():
    """
    Proporciona una sesión de BD en memoria para tests.
    
    Crea una BD SQLite temporal, crea todas las tablas,
    y la limpia después de cada test.
    """
    # BD en memoria para tests
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    # Crear todas las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Crear session factory
    async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    )

    async with async_session_maker() as session:
        yield session

    # Limpiar
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def test_client():
    """Proporciona un cliente de test para la API."""
    from fastapi.testclient import TestClient
    return TestClient(app)


# Ejemplo de cómo escribir tests:
#
# @pytest.mark.asyncio
# async def test_create_user(test_db_session):
#     """Test para crear un usuario."""
#     from app.services import user_service
#     
#     user = await user_service.create(
#         test_db_session,
#         {
#             "email": "test@example.com",
#             "full_name": "Test User",
#             "password_hash": "hashed_password",
#         }
#     )
#     
#     assert user.id is not None
#     assert user.email == "test@example.com"
