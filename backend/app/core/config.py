"""
Configuración centralizada de la aplicación.

Práctica aplicada: Configuration Management
- Uso de pydantic-settings para validación de variables de entorno
- Separación de configuración por ambientes
- Type hints para mayor seguridad
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # API Configuration
    API_TITLE: str = "Vibi API"
    API_DESCRIPTION: str = "API para plataforma de reserva de alojamientos"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database Configuration
    DATABASE_URL: str = "sqlite+aiosqlite:///./vibi.db"
    ECHO_SQL: bool = False  # Log de queries SQL

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security (se agregará en versión con autenticación)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Configuración de pydantic."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
