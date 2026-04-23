# Roadmap & Extensiones Futuras

## Resumen

Este documento detalla cómo extender la API actual con features avanzadas.

---

## 1. Autenticación JWT (Priority: ⭐⭐⭐ Alta)

### Descripción
Reemplazar el parámetro `?owner_id` con autenticación JWT segura.

### Archivos a crear
```
app/core/auth.py          # Lógica de JWT
app/schemas/auth.py       # Schemas de autenticación
app/api/routes/auth.py    # Endpoints de login
```

### Ejemplo de implementación

**app/core/auth.py:**
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crea un JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extrae el usuario del token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

**Cambios en routes:**
```python
# Antes:
@router.post("")
async def create_property(
    property_in: PropertyCreate,
    owner_id: int,  # ❌ No seguro
    session: AsyncSession = Depends(get_db_session),
):

# Después:
@router.post("")
async def create_property(
    property_in: PropertyCreate,
    current_user: User = Depends(get_current_user),  # ✅ Seguro
    session: AsyncSession = Depends(get_db_session),
):
    property_data = property_in.model_dump()
    property_data["owner_id"] = current_user.id  # Obtener del JWT
```

---

## 2. Autorización basada en Roles (Priority: ⭐⭐⭐ Alta)

### Tipos de roles
```python
class UserRole(str, Enum):
    ADMIN = "admin"          # Acceso total
    HOST = "host"            # Puede crear propiedades
    GUEST = "guest"          # Solo puede hacer reservas
```

### Decorador de autorización
```python
from functools import wraps

def require_role(*roles: UserRole):
    """Decorador para validar roles."""
    async def decorator(func):
        async def wrapper(current_user: User = Depends(get_current_user), *args, **kwargs):
            if current_user.role not in roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Uso:
@router.post("")
@require_role(UserRole.HOST)
async def create_property(...):
    # Solo hosts pueden crear propiedades
    pass
```

---

## 3. Sistema de Pagos (Priority: ⭐⭐ Media)

### Integración con Stripe

**Dependencias:**
```bash
pip install stripe
```

**app/services/payment.py:**
```python
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    """Servicio para procesamiento de pagos."""
    
    async def create_payment_intent(self, booking_id: int, amount: float):
        """Crea un intent de pago en Stripe."""
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # En centavos
            currency="eur",
            metadata={"booking_id": booking_id}
        )
        return intent

    async def confirm_payment(self, payment_intent_id: str):
        """Confirma un pago."""
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        if intent.status == "succeeded":
            return True
        return False
```

**Flujo de pago:**
```
1. Usuario crea reserva (PENDING)
2. API crea intent de pago
3. Cliente obtiene client_secret
4. Cliente confirma pago con Stripe
5. Webhook de Stripe confirma la reserva
```

---

## 4. Notificaciones por Email (Priority: ⭐⭐ Media)

### Con Celery + Redis

**Dependencias:**
```bash
pip install celery redis python-multipart aiosmtplib
```

**app/services/email.py:**
```python
from celery import Celery
from email.mime.text import MIMEText

celery_app = Celery('vibi', broker='redis://localhost')

@celery_app.task
def send_confirmation_email(user_email: str, booking_id: int):
    """Envía email de confirmación de reserva."""
    # Enviar email asincronamente
    pass

# Uso en routes:
@router.post("/bookings/{booking_id}/confirm")
async def confirm_booking(booking_id: int):
    booking = await booking_service.get_by_id(booking_id)
    booking = await booking_service.update(booking, {"status": "confirmed"})
    
    # Enviar email de forma asincróna
    send_confirmation_email.delay(booking.guest.email, booking_id)
    
    return booking
```

---

## 5. Búsqueda Avanzada con Elasticsearch (Priority: ⭐ Baja)

### Instalación
```bash
docker run -d -p 9200:9200 -e discovery.type=single-node docker.elastic.co/elasticsearch/elasticsearch:7.14.0
pip install elasticsearch
```

### Implementación
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(["localhost:9200"])

class PropertySearchService:
    """Búsqueda avanzada con Elasticsearch."""
    
    async def search(self, query: str, filters: dict):
        """Búsqueda full-text."""
        results = es.search(index="properties", body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description", "city"]
                }
            }
        })
        return results
```

---

## 6. Caché con Redis (Priority: ⭐ Baja)

```python
from redis import Redis
import json

redis_client = Redis(host='localhost', port=6379, db=0)

class CacheService:
    """Servicio de caché para mejorar performance."""
    
    async def get_property_cache(self, property_id: int):
        cached = redis_client.get(f"property:{property_id}")
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_property(self, property_id: int, data: dict):
        redis_client.setex(
            f"property:{property_id}",
            3600,  # 1 hora
            json.dumps(data)
        )
```

---

## 7. Rate Limiting (Priority: ⭐ Baja)

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("/bookings")
@limiter.limit("5/minute")
async def create_booking(request: Request, ...):
    # Máximo 5 reservas por minuto por IP
    pass
```

---

## 8. Sistema de Reviews & Ratings (Priority: ⭐⭐ Media)

### Modelo
```python
class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    rating = Column(Integer)  # 1-5 estrellas
    comment = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Service
```python
class ReviewService(BaseService[Review]):
    async def get_average_rating(self, property_id: int):
        """Calcula rating promedio."""
        reviews = await self.get_by_property(property_id)
        if not reviews:
            return 0
        avg = sum(r.rating for r in reviews) / len(reviews)
        return avg
```

---

## 9. Dashboard Admin (Priority: ⭐ Baja)

### Endpoints de administración
```python
@router.get("/admin/statistics")
@require_role(UserRole.ADMIN)
async def get_statistics():
    """Estadísticas de la plataforma."""
    return {
        "total_users": await user_service.count_all(),
        "total_properties": await property_service.count_all(),
        "total_revenue": await booking_service.calculate_revenue(),
        "active_bookings": await booking_service.count_active(),
    }
```

---

## 10. Mensajería en Tiempo Real (Priority: ⭐ Muy Baja)

### Con WebSockets
```python
from fastapi import WebSocket

@router.websocket("/ws/chat/{booking_id}")
async def websocket_endpoint(websocket: WebSocket, booking_id: int):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Guardar mensaje en BD
        # Enviar a ambos usuarios
```

---

## Prioridad de Implementación

| Feature | Priority | Effort | Impact |
|---------|----------|--------|--------|
| JWT Auth | ⭐⭐⭐ | 🔴 Medium | 🟢 Critical |
| Role-based Auth | ⭐⭐⭐ | 🔴 Medium | 🟢 Critical |
| Pagos (Stripe) | ⭐⭐ | 🟠 High | 🟢 Critical |
| Emails | ⭐⭐ | 🟢 Low | 🟡 Important |
| Búsqueda avanzada | ⭐ | 🟠 High | 🟡 Nice-to-have |
| Caché | ⭐ | 🟢 Low | 🟡 Nice-to-have |
| Rate Limiting | ⭐ | 🟢 Low | 🟡 Nice-to-have |
| Reviews | ⭐⭐ | 🔴 Medium | 🟡 Important |
| Admin Dashboard | ⭐ | 🟠 High | 🟡 Nice-to-have |
| Mensajería | ⭐ | 🟠 High | 🔴 Optional |

---

## Dependencias Recomendadas por Feature

```bash
# JWT
pip install python-jose[cryptography] passlib[bcrypt]

# Pagos
pip install stripe

# Emails
pip install celery redis aiosmtplib

# Búsqueda
pip install elasticsearch

# Caché
pip install redis

# Rate Limiting
pip install slowapi

# Tiempo Real
pip install websockets
```

---

## Estructura de Carpetas Expandida

```
vibi-backend/
├── app/
│   ├── core/
│   │   ├── auth.py           ← NEW: JWT & Autenticación
│   │   ├── security.py       ← NEW: Hashing & Seguridad
│   │   └── cache.py          ← NEW: Redis Caché
│   ├── services/
│   │   ├── payment.py        ← NEW: Stripe
│   │   ├── email.py          ← NEW: Celery + SMTP
│   │   ├── review.py         ← NEW: Reviews
│   │   └── search.py         ← NEW: Elasticsearch
│   ├── api/routes/
│   │   ├── auth.py           ← NEW: Login/Register
│   │   ├── payments.py       ← NEW: Webhook Stripe
│   │   ├── reviews.py        ← NEW: Reviews
│   │   └── admin.py          ← NEW: Admin endpoints
│   └── models/
│        ├── review.py        ← NEW
│        ├── payment.py       ← NEW
│        └── message.py       ← NEW
└── ...
```

---

## Resumen

La API actual es **sólida y escalable**. El siguiente paso importante es:

1. **JWT Auth** → Asegurar endpoints
2. **Payments** → Monetizar
3. **Emails** → Mejorar UX
4. **Reviews** → Confianza de usuarios

El resto son optimizaciones y features opcionales.
