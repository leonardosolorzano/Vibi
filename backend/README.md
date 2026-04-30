# Vibi API - Backend

Backend moderno y escalable para una plataforma de reserva de alojamientos construido con **FastAPI**.

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Requisitos](#requisitos)
4. [Instalación](#instalación)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Configuración](#configuración)
7. [Ejecución](#ejecución)
8. [API Endpoints](#api-endpoints)
9. [Buenas Prácticas Implementadas](#buenas-prácticas-implementadas)
10. [Patrones de Diseño](#patrones-de-diseño)
11. [Seguridad](#seguridad)
12. [Testing](#testing)
13. [Deployment](#deployment)
14. [Roadmap](#roadmap)

---

## 📌 Descripción General

**Vibi API** es un backend robusto y profesional para una plataforma de reserva de alojamientos similar a Airbnb. Proporciona funcionalidades completas para:

- Gestión de usuarios (hosts y guests)
- Gestión de propiedades/alojamientos
- Reservas con validación de disponibilidad
- Cálculo automático de precios
- Búsqueda avanzada con múltiples criterios

**Stack Tecnológico:**
- **Framework:** FastAPI (async)
- **Base de Datos:** PostgreSQL + SQLAlchemy ORM
- **Validación:** Pydantic v2
- **Autenticación:** JWT (implementación futura)
- **Testing:** Pytest + AsyncIO

---

## ✨ Características

### ✅ Implementadas

- [x] CRUD completo para Usuarios, Propiedades y Reservas
- [x] Validación avanzada de datos con Pydantic
- [x] Búsqueda y filtrado de propiedades
- [x] Validación de disponibilidad de fechas
- [x] Cálculo automático de precios
- [x] Gestión de estados de reserva
- [x] Documentación interactiva (Swagger UI)
- [x] Manejo centralizado de errores
- [x] Inyección de dependencias

### 🔜 Por Implementar

- [ ] Autenticación con JWT
- [ ] Autorización basada en roles
- [ ] Paginación optimizada
- [ ] Caché con Redis
- [ ] Búsqueda avanzada con Elasticsearch
- [ ] Sistema de pagos (Stripe/PayPal)
- [ ] Notificaciones por email
- [ ] Rate limiting
- [ ] Tests automatizados
- [ ] CI/CD pipeline

---

## 📦 Requisitos

- Python >= 3.10
- PostgreSQL >= 12
- uv (gestión de entorno y dependencias)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/vibi-backend.git
cd vibi-backend
```

### 2. Crear entorno e instalar dependencias con uv

```bash
# Crear .venv y sincronizar dependencias de runtime
uv sync

# Incluir también dependencias de desarrollo y testing
uv sync --dev
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus valores
nano .env
```

**Variables obligatorias en .env:**
```ini
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/vibi_db
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui
```

### 4. Crear base de datos

```bash
# Crear BD (en PostgreSQL)
createdb vibi_db

# Las tablas se crean automáticamente al iniciar la aplicación
```

---

## 📁 Estructura del Proyecto

```
vibi-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── users.py        # CRUD de usuarios
│   │       ├── properties.py   # CRUD de propiedades
│   │       └── bookings.py     # CRUD de reservas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración de la app
│   │   └── database.py         # Configuración de BD
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # Modelo ORM User
│   │   ├── property.py         # Modelo ORM Property
│   │   └── booking.py          # Modelo ORM Booking
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Validación User (Pydantic)
│   │   ├── property.py         # Validación Property (Pydantic)
│   │   └── booking.py          # Validación Booking (Pydantic)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py             # Servicio genérico CRUD
│   │   ├── user.py             # Lógica de negocio User
│   │   ├── property.py         # Lógica de negocio Property
│   │   └── booking.py          # Lógica de negocio Booking
│   └── database/               # (Pendiente: migraciones con Alembic)
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures de pytest
│   ├── test_users.py
│   ├── test_properties.py
│   └── test_bookings.py
├── pyproject.toml              # Configuración del proyecto
├── README.md                   # Este archivo
├── .env.example                # Variables de entorno de ejemplo
├── .gitignore
└── uv.lock                     # Lockfile de dependencias (uv)
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)

```ini
# API Configuration
API_TITLE=Vibi API
API_DESCRIPTION=API para plataforma de reserva de alojamientos
API_VERSION=1.0.0
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql://vibi_user:vibi_password@localhost:5432/vibi_db
ECHO_SQL=False  # Log de queries SQL (solo desarrollo)

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Archivo de Configuración (app/core/config.py)

La configuración utiliza **Pydantic Settings** para:
- Cargar automáticamente variables de entorno
- Validar tipos de datos
- Proporcionar valores por defecto seguros

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    # ...

settings = Settings()
```

---

## 🏃 Ejecución

### Modo Desarrollo

```bash
# Recomendado con uv + FastAPI CLI
uv run fastapi dev main.py

# Con uvicorn directamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O con python -m
python -m uvicorn app.main:app --reload
```

**URL local:** http://localhost:8000

### Acceder a Documentación

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Modo Producción

```bash
# Con gunicorn + uvicorn workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Usuarios (`/users`)

#### Crear usuario
```http
POST /api/v1/users
Content-Type: application/json

{
  "email": "usuario@example.com",
  "full_name": "Juan Pérez",
  "password": "contraseña_segura_123",
  "phone": "+34612345678"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "full_name": "Juan Pérez",
  "phone": "+34612345678",
  "is_active": true,
  "created_at": "2024-04-23T10:30:00",
  "updated_at": "2024-04-23T10:30:00"
}
```

#### Listar usuarios
```http
GET /api/v1/users?skip=0&limit=10
```

#### Obtener usuario específico
```http
GET /api/v1/users/{user_id}
```

#### Actualizar usuario
```http
PUT /api/v1/users/{user_id}
Content-Type: application/json

{
  "full_name": "Juan Carlos Pérez",
  "phone": "+34687654321"
}
```

#### Eliminar usuario
```http
DELETE /api/v1/users/{user_id}
```

---

### Propiedades (`/properties`)

#### Crear propiedad
```http
POST /api/v1/properties?owner_id=1
Content-Type: application/json

{
  "title": "Apartamento acogedor en Barcelona",
  "description": "Hermoso apartamento de 2 habitaciones en el Eixample...",
  "property_type": "apartment",
  "price_per_night": 85.50,
  "city": "Barcelona",
  "address": "Passeig de Gràcia 132, Barcelona",
  "max_guests": 4,
  "bedrooms": 2,
  "bathrooms": 1
}
```

#### Búsqueda avanzada
```http
GET /api/v1/properties?city=Barcelona&property_type=apartment&min_price=50&max_price=150&min_guests=4
```

**Parámetros de búsqueda:**
- `city` - Ciudad (búsqueda parcial)
- `property_type` - Tipo (apartment, house, villa, cabin, loft)
- `min_price` - Precio mínimo por noche
- `max_price` - Precio máximo por noche
- `min_guests` - Mínimo de huéspedes soportados
- `skip` - Registros a saltar (default: 0)
- `limit` - Máximo de registros (default: 100)

#### Obtener detalles de propiedad
```http
GET /api/v1/properties/{property_id}
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Apartamento acogedor en Barcelona",
  "description": "...",
  "property_type": "apartment",
  "price_per_night": 85.50,
  "city": "Barcelona",
  "address": "Passeig de Gràcia 132",
  "max_guests": 4,
  "bedrooms": 2,
  "bathrooms": 1,
  "owner_id": 1,
  "owner": {
    "id": 1,
    "email": "host@example.com",
    "full_name": "Host Name",
    "is_active": true
  },
  "is_active": true,
  "created_at": "2024-04-23T10:30:00",
  "updated_at": "2024-04-23T10:30:00"
}
```

#### Propiedades de un host
```http
GET /api/v1/properties/owner/{owner_id}/properties
```

---

### Reservas (`/bookings`)

#### Crear reserva
```http
POST /api/v1/bookings?guest_id=2
Content-Type: application/json

{
  "property_id": 1,
  "check_in_date": "2024-05-10T15:00:00",
  "check_out_date": "2024-05-15T11:00:00",
  "number_of_guests": 2,
  "notes": "Llegada con retraso"
}
```

**Validaciones:**
- Propiedad debe existir
- Fechas de salida > fechas de entrada
- Huéspedes ≤ capacidad máxima
- No hay conflicto de fechas

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "property_id": 1,
  "guest_id": 2,
  "check_in_date": "2024-05-10T15:00:00",
  "check_out_date": "2024-05-15T11:00:00",
  "number_of_guests": 2,
  "total_price": 427.50,
  "status": "pending",
  "notes": "Llegada con retraso",
  "created_at": "2024-04-23T12:00:00",
  "updated_at": "2024-04-23T12:00:00"
}
```

#### Listar reservas (con filtros)
```http
# Todas las reservas
GET /api/v1/bookings

# Reservas de una propiedad
GET /api/v1/bookings?property_id=1

# Reservas de un huésped
GET /api/v1/bookings?guest_id=2

# Reservas por estado
GET /api/v1/bookings?status=confirmed
```

**Estados disponibles:**
- `pending` - Pendiente de confirmación
- `confirmed` - Confirmada
- `cancelled` - Cancelada
- `completed` - Completada

#### Obtener detalles de reserva
```http
GET /api/v1/bookings/{booking_id}
```

#### Actualizar reserva
```http
PUT /api/v1/bookings/{booking_id}?guest_id=2
Content-Type: application/json

{
  "check_in_date": "2024-05-11T15:00:00",
  "check_out_date": "2024-05-16T11:00:00",
  "notes": "Cambio de fechas"
}
```

**Nota:** Si se cambian las fechas, se revalida disponibilidad y se recalcula el precio.

#### Confirmar reserva
```http
PATCH /api/v1/bookings/{booking_id}/confirm
```

#### Cancelar reserva
```http
DELETE /api/v1/bookings/{booking_id}?guest_id=2
```

#### Verificar disponibilidad
```http
GET /api/v1/bookings/property/{property_id}/availability
```

**Respuesta:**
```json
{
  "property_id": 1,
  "reserved_dates": [
    {
      "check_in": "2024-05-10T15:00:00",
      "check_out": "2024-05-15T11:00:00"
    },
    {
      "check_in": "2024-06-01T15:00:00",
      "check_out": "2024-06-08T11:00:00"
    }
  ]
}
```

---

## 🏛️ Buenas Prácticas Implementadas

### 1. **Architecture & Project Structure**

✅ **Separación de Responsabilidades:**
- Routes → Manejo de HTTP
- Services → Lógica de negocio
- Models → Entidades ORM
- Schemas → Validación de datos

✅ **Modularidad:**
- Cada ruta en su propio archivo
- Cada servicio enfocado en una entidad
- Importaciones centralizadas en `__init__.py`

### 2. **Database Design**

✅ **Relaciones Claras:**
```
User (1) ─── (N) Property (Propiedades del propietario)
User (1) ─── (N) Booking (Reservas del huésped)
Property (1) ─── (N) Booking (Reservas de la propiedad)
```

✅ **Índices para Performance:**
```python
id = Column(Integer, primary_key=True, index=True)
email = Column(String(255), unique=True, nullable=False, index=True)
city = Column(String(100), nullable=False, index=True)
```

✅ **Auditoría con Timestamps:**
```python
created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
updated_at = Column(DateTime, ..., onupdate=datetime.utcnow, nullable=False)
```

✅ **Integridad Referencial:**
```python
owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
```

### 3. **API Design (RESTful)**

✅ **Convenciones HTTP:**
- `POST /resource` → Crear
- `GET /resource` → Listar
- `GET /resource/{id}` → Obtener
- `PUT /resource/{id}` → Actualizar
- `DELETE /resource/{id}` → Eliminar
- `PATCH /resource/{id}/action` → Acción específica

✅ **Códigos de Estado Apropiados:**
- `201 Created` → Creación exitosa
- `400 Bad Request` → Validación fallida
- `403 Forbidden` → Sin permisos
- `404 Not Found` → Recurso no existe
- `204 No Content` → Eliminación exitosa

✅ **Versionado de API:**
```
/api/v1/users
/api/v1/properties
/api/v1/bookings
```

### 4. **Data Validation**

✅ **Schemas Pydantic Separados:**
- `UserCreate` - Solo campos para creación
- `UserUpdate` - Campos opcionales para actualización
- `UserResponse` - Respuesta al cliente (sin datos sensibles)

✅ **Validaciones en Múltiples Capas:**
```python
# Schema: Validación estructural
class BookingCreate(BaseModel):
    check_out_date: datetime
    
    @field_validator("check_out_date")
    def check_out_after_check_in(cls, v, info):
        if v <= info.data["check_in_date"]:
            raise ValueError("check_out > check_in")

# Service: Validación de negocio
is_available = await booking_service.check_availability(...)
```

✅ **Validaciones por Campo:**
- Rangos: `Field(..., ge=1, le=100)`
- Longitud: `Field(..., min_length=1, max_length=255)`
- Patrones: `EmailStr` en email

### 5. **Error Handling**

✅ **Excepciones HTTP Específicas:**
```python
# No encontrado
raise HTTPException(status_code=404, detail="Usuario no encontrado")

# No autorizado
raise HTTPException(status_code=403, detail="Sin permisos")

# Validación
raise HTTPException(status_code=400, detail="Propiedad no disponible")
```

✅ **Mensajes Descriptivos:**
```python
raise HTTPException(
    status_code=400,
    detail=f"La propiedad soporta máximo {property_obj.max_guests} huéspedes"
)
```

### 6. **Business Logic**

✅ **Cálculo de Precio Automático:**
```python
async def calculate_total_price(self, session, property_id, check_in, check_out):
    nights = (check_out - check_in).days
    return property_obj.price_per_night * nights
```

✅ **Validación de Disponibilidad:**
```python
async def check_availability(self, session, property_id, check_in, check_out):
    # Detecta overlaps con reservas existentes
    conditions = [
        self.model.property_id == property_id,
        self.model.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING]),
        self.model.check_in_date < check_out,
        self.model.check_out_date > check_in,
    ]
```

✅ **Validación de Ownership:**
```python
if booking.guest_id != guest_id:
    raise HTTPException(status_code=403, detail="No autorizado")
```

### 7. **Type Safety**

✅ **Type Hints Completos:**
```python
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    ...
```

✅ **Generics para Reutilización:**
```python
class BaseService(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
```

### 8. **Dependency Injection**

✅ **FastAPI Depends():**
```python
@router.get("/users")
async def get_users(
    session: AsyncSession = Depends(get_db_session),
):
    # session se inyecta automáticamente
```

✅ **Inyección de Servicios Singleton:**
```python
user_service = UserService()  # Una instancia para toda la app
```

### 9. **Configuration Management**

✅ **Variables Centralizadas:**
```python
from app.core.config import settings
DATABASE_URL = settings.DATABASE_URL
```

✅ **Valores por Defecto Seguros:**
```python
DEBUG: bool = False
SECRET_KEY: str = "change-in-production"
```

### 10. **Documentation**

✅ **Docstrings Detallados:**
```python
async def check_availability(
    self,
    session: AsyncSession,
    property_id: int,
    check_in: datetime,
    check_out: datetime,
) -> bool:
    """
    Verifica si una propiedad está disponible.
    
    Args:
        session: Sesión de BD
        property_id: ID de la propiedad
        check_in: Fecha de entrada
        check_out: Fecha de salida
    
    Returns:
        True si disponible, False si no
    """
```

✅ **Documentación OpenAPI Automática:**
```python
@router.post(
    "",
    response_model=BookingResponse,
    status_code=201,
    summary="Crear una nueva reserva",
)
async def create_booking(...):
    """Crea una nueva reserva con validaciones de disponibilidad."""
```

✅ **Swagger UI Automático:**
- Accesible en `/docs`
- Prueba endpoints directamente
- Ver esquemas de datos

### 11. **Async/Await & Performance**

✅ **Operaciones Asíncronas:**
```python
async def get_users(session: AsyncSession = Depends(get_db_session)):
    return await user_service.get_all(session)
```

✅ **Pool de Conexiones:**
```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Valida conexiones
)
```

### 12. **Security Best Practices**

✅ **Ocultamiento de Datos Sensibles:**
```python
class UserResponse(UserBase):
    # No incluye password_hash
    id: int
    is_active: bool
```

✅ **Validación de Ownership:**
```python
if property_obj.owner_id != owner_id:
    raise HTTPException(403, "No autorizado")
```

✅ **CORS Configurado:**
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

---

## 🎨 Patrones de Diseño

### 1. **Repository Pattern**

`BaseService` actúa como repositorio genérico:

```
Entity (DB)
    ↓
Service (BaseService + Specialized Service)
    ↓
Route (HTTP Handler)
    ↓
Client
```

### 2. **Dependency Injection**

Inyección de sesión de BD:

```python
def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

@router.get("/users")
async def get_users(session: AsyncSession = Depends(get_db_session)):
    ...
```

### 3. **Factory Pattern**

Creación de sesiones:

```python
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

### 4. **Strategy Pattern**

Servicios especializados según entidad:

```
BaseService (estrategia general)
├── UserService (estrategia específica)
├── PropertyService (estrategia específica)
└── BookingService (estrategia específica)
```

### 5. **Template Method**

Métodos comunes en BaseService:

```python
class BaseService(Generic[T]):
    async def create(self, session, obj_in): ...
    async def get_by_id(self, session, id): ...
    async def update(self, session, db_obj, obj_in): ...
    async def delete(self, session, id): ...
```

---

## 🔒 Seguridad

### Implementado

- ✅ Almacenamiento seguro de contraseñas (con hash)
- ✅ Validación de ownership de recursos
- ✅ CORS configurado
- ✅ Type hints para evitar errores
- ✅ Variables de entorno para secretos

### Por Implementar

- [ ] JWT para autenticación
- [ ] OAuth2 con password flow
- [ ] Roles y permisos (RBAC)
- [ ] Rate limiting
- [ ] HTTPS enforcement
- [ ] CSRF protection
- [ ] SQL injection prevention (SQLAlchemy)
- [ ] XSS prevention

### Checklist de Seguridad

```ini
[ ] Cambiar SECRET_KEY en producción
[ ] Habilitar HTTPS
[ ] Restringir CORS a dominios específicos
[ ] Implementar autenticación JWT
[ ] Usar bcrypt para hashing
[ ] Implementar rate limiting
[ ] Logs de auditoría
[ ] Validar inputs en cliente
[ ] Headers de seguridad
[ ] Monitoreo de errores
```

---

## 🧪 Testing

### Estructura de Tests

```
tests/
├── conftest.py          # Fixtures compartidas
├── test_users.py
├── test_properties.py
└── test_bookings.py
```

### Ejemplo de Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_user():
    response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "securepass123",
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

### Ejecutar Tests

```bash
# Todos los tests
uv run pytest

# Con cobertura
uv run pytest --cov=app

# Modo verbose
uv run pytest -vv

# Tests específicos
uv run pytest tests/test_bookings.py::test_create_booking
```

---

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: vibi_db
      POSTGRES_USER: vibi_user
      POSTGRES_PASSWORD: vibi_password
    ports:
      - "5432:5432"

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://vibi_user:vibi_password@db:5432/vibi_db
```

### Variables en Producción

```ini
DEBUG=False
SECRET_KEY=<generar-con-secrets.token_urlsafe()>
DATABASE_URL=postgresql://user:pass@prod-db:5432/vibi_db
ALLOWED_HOSTS=api.vibi.com
CORS_ORIGINS=https://vibi.com,https://app.vibi.com
```

---

## 📈 Roadmap

### Phase 1 (v1.0 - Actual) ✅
- [x] CRUD básico
- [x] Validación de disponibilidad
- [x] Búsqueda avanzada
- [x] Cálculo de precios

### Phase 2 (v1.1)
- [ ] Autenticación JWT
- [ ] Sistema de pagos
- [ ] Notificaciones email
- [ ] Reviews y ratings

### Phase 3 (v1.2)
- [ ] Admin panel
- [ ] Analytics
- [ ] Reportes
- [ ] Dashboard

### Phase 4 (v2.0)
- [ ] Mensajería en tiempo real
- [ ] Video calls
- [ ] Seguros
- [ ] Arbitraje

---

## 📞 Contacto & Soporte

- **Issues:** [GitHub Issues](https://github.com/tu-usuario/vibi-backend/issues)
- **Email:** tu-email@example.com
- **Documentación:** http://localhost:8000/docs

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE`.

---

## 👥 Contribuidores

- Tu nombre - Creador principal

---

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- SQLAlchemy por el ORM robusto
- Pydantic por la validación
- La comunidad Python

---

**Última actualización:** 23 de Abril de 2024
