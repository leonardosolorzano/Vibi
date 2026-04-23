"""
Configuración de la base de datos y sesiones.

Práctica aplicada: Database Session Management
- Uso de SQLAlchemy ORM para operaciones de BD
- Patrón de sesión con context manager
- Dependency injection para sesiones
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Base para todos los modelos
Base = declarative_base()


def _normalize_database_url(url: str) -> str:
    """
    Normaliza URLs de base de datos para uso asíncrono con SQLAlchemy.

    Convierte:
    - postgresql://... -> postgresql+asyncpg://...
    - postgres://...   -> postgresql+asyncpg://...
    """
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


database_url = _normalize_database_url(settings.DATABASE_URL)

# Engine asíncrono
engine = create_async_engine(
    database_url,
    echo=settings.ECHO_SQL,
    future=True,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
)

# Factory de sesiones
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para inyectar la sesión de BD en los endpoints.

    Yields:
        AsyncSession: Sesión de base de datos asíncrona.

    Example:
        @router.get("/items")
        async def get_items(session: AsyncSession = Depends(get_db_session)):
            # session está disponible y se cierra automáticamente
            pass
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas.

    Se ejecuta al inicio de la aplicación.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Cierra la conexión con la base de datos."""
    await engine.dispose()
