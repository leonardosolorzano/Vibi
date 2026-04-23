"""
Guía de Inicio Rápido - Desarrollo Local

Este archivo contiene instrucciones para ejecutar rápidamente el proyecto en desarrollo.
"""

# ============================================================================
# PASO 1: Preparar el Entorno
# ============================================================================

# 1. Crear y activar entorno virtual (desde la raíz del proyecto)
#    En Linux/Mac:
#    python -m venv .venv
#    source .venv/bin/activate
#
#    En Windows:
#    python -m venv .venv
#    .venv\Scripts\activate

# 2. Instalar dependencias
#    pip install -r requirements.txt

# 3. Crear archivo .env (copiar desde .env.example)
#    cp .env.example .env

# 4. Editar .env con tu configuración local
#    DATABASE_URL=postgresql://tu_usuario:tu_password@localhost:5432/vibi_db


# ============================================================================
# PASO 2: Base de Datos
# ============================================================================

# 1. Asegúrate que PostgreSQL está corriendo
#    En Linux/Mac: sudo service postgresql start
#    En Docker: docker run -d -e POSTGRES_PASSWORD=password postgres

# 2. Crear la base de datos (opcional, FastAPI la crea automáticamente)
#    createdb vibi_db

# 3. Las tablas se crean automáticamente al iniciar FastAPI


# ============================================================================
# PASO 3: Ejecutar la Aplicación
# ============================================================================

# Opción 1: Uvicorn directo (recomendado para desarrollo)
#    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Python -m
#    python -m uvicorn app.main:app --reload

# La aplicación estará disponible en: http://localhost:8000


# ============================================================================
# PASO 4: Acceder a la Documentación
# ============================================================================

# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - OpenAPI JSON: http://localhost:8000/openapi.json


# ============================================================================
# EJEMPLOS DE USO CON cURL
# ============================================================================

# 1. Crear usuario
#    curl -X POST "http://localhost:8000/api/v1/users" \
#      -H "Content-Type: application/json" \
#      -d '{
#        "email": "usuario@example.com",
#        "full_name": "Juan Pérez",
#        "password": "contraseña_segura_123"
#      }'

# 2. Listar usuarios
#    curl "http://localhost:8000/api/v1/users"

# 3. Crear propiedad (parámetro owner_id)
#    curl -X POST "http://localhost:8000/api/v1/properties?owner_id=1" \
#      -H "Content-Type: application/json" \
#      -d '{
#        "title": "Apartamento en Barcelona",
#        "description": "Hermoso apartamento...",
#        "property_type": "apartment",
#        "price_per_night": 85.50,
#        "city": "Barcelona",
#        "address": "Calle Principal 123",
#        "max_guests": 4,
#        "bedrooms": 2,
#        "bathrooms": 1
#      }'

# 4. Buscar propiedades
#    curl "http://localhost:8000/api/v1/properties?city=Barcelona&property_type=apartment"

# 5. Crear reserva (parámetro guest_id)
#    curl -X POST "http://localhost:8000/api/v1/bookings?guest_id=2" \
#      -H "Content-Type: application/json" \
#      -d '{
#        "property_id": 1,
#        "check_in_date": "2024-05-10T15:00:00",
#        "check_out_date": "2024-05-15T11:00:00",
#        "number_of_guests": 2
#      }'


# ============================================================================
# ÚTIL: Crear datos de prueba rápidamente
# ============================================================================

# Script Python para popular la BD con datos de prueba:
# from app.services import user_service, property_service, booking_service
# from app.core.database import async_session_maker
# from datetime import datetime, timedelta
#
# async def create_test_data():
#     async with async_session_maker() as session:
#         # Crear usuarios
#         user1 = await user_service.create(session, {
#             "email": "host@example.com",
#             "full_name": "Carlos Host",
#             "password_hash": user_service.hash_password("password123"),
#             "is_active": True
#         })
#         
#         user2 = await user_service.create(session, {
#             "email": "guest@example.com",
#             "full_name": "María Guest",
#             "password_hash": user_service.hash_password("password123"),
#             "is_active": True
#         })
#         
#         # Crear propiedad
#         property1 = await property_service.create(session, {
#             "title": "Apartamento",
#             "description": "Bonito apartamento",
#             "property_type": "apartment",
#             "price_per_night": 100,
#             "city": "Barcelona",
#             "address": "Calle X",
#             "max_guests": 4,
#             "bedrooms": 2,
#             "bathrooms": 1,
#             "owner_id": user1.id,
#             "is_active": True
#         })
#         
#         # Crear reserva
#         booking1 = await booking_service.create(session, {
#             "property_id": property1.id,
#             "guest_id": user2.id,
#             "check_in_date": datetime.utcnow() + timedelta(days=5),
#             "check_out_date": datetime.utcnow() + timedelta(days=10),
#             "number_of_guests": 2,
#             "total_price": 500,
#             "status": "confirmed"
#         })
#         
#         await session.commit()


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# Problema: ModuleNotFoundError
# Solución: Asegúrate que estás en la raíz del proyecto y que .venv está activado

# Problema: Connection refused (postgresql)
# Solución: Inicia PostgreSQL
#    Linux: sudo service postgresql start
#    Mac: brew services start postgresql
#    Windows: Inicia el servicio desde Servicios

# Problema: Tabla ya existe
# Solución: Elimina la BD y déjala recrear
#    dropdb vibi_db
#    createdb vibi_db

# Problema: Puerto 8000 ocupado
# Solución: Usa otro puerto
#    uvicorn app.main:app --port 8001


# ============================================================================
# PRÓXIMOS PASOS
# ============================================================================

# 1. Explorar la documentación Swagger en /docs
# 2. Crear usuarios de prueba
# 3. Crear propiedades
# 4. Probar creación de reservas
# 5. Estudiar el código de services/ para entender la lógica
# 6. Implementar tests en tests/
# 7. Agregar autenticación JWT en app/core/auth.py
