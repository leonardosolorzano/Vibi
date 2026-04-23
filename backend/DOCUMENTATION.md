# 📚 Documentación - Índice

Bienvenido a la documentación completa de **Vibi API**. Este índice te ayudará a navegar.

## 🚀 Para Empezar Rápido

1. **[QUICKSTART.md](QUICKSTART.md)** ← **EMPIEZA AQUÍ**
   - Instalación en 5 minutos
   - Ejecutar en local
   - Ejemplos con cURL

2. **[README.md](README.md)**
   - Descripción general del proyecto
   - Características principales
   - Toda la documentación de API
   - Endpoints y ejemplos detallados

## 📖 Documentación Completa

### Por Nivel de Experiencia

#### Principiante
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- [README.md](README.md) - Visión general
- [API Endpoints](README.md#-api-endpoints) - Cómo usar la API

#### Intermedio
- [Estructura del Proyecto](README.md#-estructura-del-proyecto)
- [Buenas Prácticas](README.md#-buenas-prácticas-implementadas)
- [Patrones de Diseño](README.md#-patrones-de-diseño)

#### Avanzado
- [ROADMAP.md](ROADMAP.md) - Extensiones futuras
- [DEPLOY.md](DEPLOY.md) - Deployment en producción
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribuir al proyecto

---

## 📁 Archivos de Documentación

| Archivo | Descripción | Tiempo de lectura |
|---------|-------------|-------------------|
| **QUICKSTART.md** | Instalación y primeros pasos | 5 min ⚡ |
| **README.md** | Documentación completa | 30 min 📚 |
| **ROADMAP.md** | Features futuras | 15 min 🗺️ |
| **DEPLOY.md** | Deployment en producción | 20 min 🚀 |
| **CONTRIBUTING.md** | Guía para contribuidores | 10 min 🤝 |

---

## 🎯 Guías por Tarea

### Quiero Ejecutar Localmente
→ Lee [QUICKSTART.md](QUICKSTART.md)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Quiero Entender la API
→ Lee [README.md - API Endpoints](README.md#-api-endpoints)

### Quiero Conocer la Estructura
→ Lee [README.md - Estructura](README.md#-estructura-del-proyecto)

### Quiero Agregar una Feature
→ Lee [ROADMAP.md](ROADMAP.md) y [CONTRIBUTING.md](CONTRIBUTING.md)

### Quiero Hacer Deploy en Producción
→ Lee [DEPLOY.md](DEPLOY.md)

### Quiero Contribuir al Proyecto
→ Lee [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🔑 Conceptos Clave Explicados

### Modelos (Database)
- **User** - Usuarios (hosts y guests)
- **Property** - Alojamientos/propiedades
- **Booking** - Reservas

Ver en: [Models en README](README.md#modelos-database)

### Servicios (Business Logic)
- **UserService** - Operaciones con usuarios
- **PropertyService** - Búsqueda y filtrado
- **BookingService** - Validaciones de disponibilidad

Ver en: [Services en README](README.md#servicios-business-logic)

### Routes (API Endpoints)
- `/api/v1/users` - Gestión de usuarios
- `/api/v1/properties` - Gestión de propiedades
- `/api/v1/bookings` - Gestión de reservas

Ver en: [Endpoints en README](README.md#-api-endpoints)

---

## 📋 Dependencias Principales

```
FastAPI          → Framework web
SQLAlchemy       → ORM para BD
Pydantic         → Validación de datos
PostgreSQL       → Base de datos
Uvicorn          → Servidor ASGI
```

Ver todas: [README.md - Stack Tecnológico](README.md#stack-tecnológico)

---

## 🧪 Testing

### Ejecutar Tests
```bash
pytest
pytest -vv  # verbose
pytest --cov=app  # con cobertura
```

### Ver Ejemplos de Tests
→ Lee [tests/test_bookings.py](tests/test_bookings.py)

---

## 🔒 Seguridad

### Implementado
- ✅ Validación de datos
- ✅ Ocultamiento de datos sensibles
- ✅ Validación de ownership

### Por Implementar
- [ ] JWT Authentication
- [ ] Rate Limiting
- [ ] HTTPS/SSL

Ver más: [README.md - Seguridad](README.md#-seguridad)

---

## 🚀 Deployment

### Opciones
1. **VPS** (Ubuntu + Nginx) - Más control
2. **Docker** - Portabilidad
3. **Cloud** (Heroku, Railway, etc) - Más fácil

Ver detalles: [DEPLOY.md](DEPLOY.md)

---

## 🎓 Learning Path Recomendado

### Día 1: Aprender Conceptos Básicos
1. Leer [QUICKSTART.md](QUICKSTART.md)
2. Ejecutar localmente
3. Probar endpoints en Swagger UI (/docs)

### Día 2: Entender la Arquitectura
1. Leer [README.md](README.md)
2. Explorar la estructura de carpetas
3. Entender Models, Services, Routes

### Día 3: Trabajar con el Código
1. Crear un usuario (POST /users)
2. Crear una propiedad (POST /properties)
3. Crear una reserva (POST /bookings)
4. Ver detalles (GET /bookings/1)

### Día 4: Testing
1. Leer tests en [tests/test_bookings.py](tests/test_bookings.py)
2. Escribir un test nuevo
3. Ejecutar con cobertura

### Día 5: Extensión
1. Ver [ROADMAP.md](ROADMAP.md)
2. Implementar JWT en [ROADMAP.md#1-autenticación-jwt](ROADMAP.md#1-autenticación-jwt)
3. Agregar feature nueva

---

## ❓ Preguntas Frecuentes

### ¿Por dónde empiezo?
→ [QUICKSTART.md](QUICKSTART.md)

### ¿Cómo uso la API?
→ [README.md - Endpoints](README.md#-api-endpoints)

### ¿Cómo hago deploy?
→ [DEPLOY.md](DEPLOY.md)

### ¿Cómo agrego una feature?
→ [ROADMAP.md](ROADMAP.md) y [CONTRIBUTING.md](CONTRIBUTING.md)

### ¿Qué tecnologías usa?
→ [README.md - Stack](README.md#stack-tecnológico)

---

## 📞 Contacto & Ayuda

- **Issues:** GitHub Issues
- **Documentación:** Este archivo
- **Código de ejemplo:** [tests/test_bookings.py](tests/test_bookings.py)

---

## 📈 Progreso de Lectura

```
Principiante:
[========================================] QUICKSTART.md
[========                              ] README.md (API part)

Intermedio:
[========                              ] README.md (full)
[======                                ] Architecture

Avanzado:
[========                              ] ROADMAP.md
[======                                ] DEPLOY.md
[=====                                 ] CONTRIBUTING.md
```

---

## 🎯 Próximos Pasos

### Opción 1: Ejecutar y Probar
1. Instalar según [QUICKSTART.md](QUICKSTART.md)
2. Crear datos de prueba
3. Explorar endpoints en /docs

### Opción 2: Entender el Código
1. Leer estructura en [README.md](README.md#-estructura-del-proyecto)
2. Revisar archivos en `app/models/`
3. Revisar archivos en `app/services/`

### Opción 3: Hacer Deploy
1. Leer [DEPLOY.md](DEPLOY.md)
2. Elegir plataforma (VPS, Docker, Cloud)
3. Seguir instrucciones específicas

### Opción 4: Contribuir
1. Leer [CONTRIBUTING.md](CONTRIBUTING.md)
2. Elegir feature del [ROADMAP.md](ROADMAP.md)
3. Crear PR

---

## ✅ Validación de Lectura

Después de leer la documentación, deberías poder:

- [ ] Instalar y ejecutar localmente
- [ ] Crear un usuario, propiedad y reserva
- [ ] Entender la estructura del proyecto
- [ ] Explicar qué hace cada servicio
- [ ] Escribir un test
- [ ] Desplegar en producción (teoría)
- [ ] Contribuir una feature nueva

---

## 📝 Versión de Documentación

- **Última actualización:** 23 de Abril de 2024
- **Versión:** 1.0.0
- **Documentación para:** Vibi API v1.0.0

---

## 🎉 ¡Listo!

Ahora sí, comienza con [QUICKSTART.md](QUICKSTART.md) →

¿Preguntas? Revisa la sección de [FAQ](#preguntas-frecuentes) o abre un issue.

**Happy coding! 🚀**
