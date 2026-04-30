"""
Aplicación principal de FastAPI.

Práctica aplicada: Application Factory & Event Lifecycle
- Inicialización de BD al startup
- Cierre de conexiones al shutdown
- Inclusión de routers organizados
- CORS y middleware configurables
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth_router, bookings_router, properties_router, users_router
from app.core.config import settings
from app.core.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor de contexto para eventos de ciclo de vida de la aplicación.

    - Startup: Inicializa la base de datos
    - Shutdown: Cierra conexiones
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: restringir a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(properties_router)
app.include_router(bookings_router)


@app.get("/", tags=["Health"])
async def root():
    """Endpoint raíz que verifica que la API esté funcionando."""
    return {
        "message": "Vibi API is running",
        "version": settings.API_VERSION,
        "documentation": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de healthcheck para monitoreo."""
    return {"status": "healthy", "service": "Vibi API"}
