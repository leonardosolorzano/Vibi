# Guía de Contribución

¡Gracias por querer contribuir a Vibi! Este documento explica cómo hacerlo.

## Code of Conduct

- Sé respetuoso con otros contribuidores
- Reporta bugs de forma constructiva
- Proporciona feedback educativo en PRs

## Cómo Empezar

### 1. Fork el repositorio

```bash
git clone https://github.com/tu-usuario/vibi-backend.git
cd vibi-backend
git remote add upstream https://github.com/original-repo/vibi-backend.git
```

### 2. Crear rama de feature

```bash
git checkout -b feature/nombre-descriptivo
# Ejemplos:
# git checkout -b feature/add-reviews
# git checkout -b fix/booking-validation
# git checkout -b docs/update-readme
```

### 3. Hacer cambios

- ✅ Seguir el estilo de código existente
- ✅ Agregar type hints
- ✅ Escribir docstrings
- ✅ Crear tests para nuevas features
- ✅ Actualizar README si es necesario

### 4. Ejecutar tests

```bash
pytest -vv --cov=app

# O test específico
pytest tests/test_bookings.py::TestBookings::test_create_booking_success
```

### 5. Verificar código

```bash
# Linting
flake8 app tests

# Formateo
black app tests --check

# Type checking
mypy app

# Todo junto
black app tests && flake8 app tests && mypy app
```

### 6. Commit y Push

```bash
git add .
git commit -m "feat: agregar validación de email"
git push origin feature/nombre-descriptivo
```

### 7. Crear Pull Request

- Título descriptivo: "feat:", "fix:", "docs:", etc.
- Descripción clara del cambio
- Referenciar issues: "Closes #123"
- Agregar screenshots si hay cambios visuales

## Convenciones

### Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: agregar nueva feature
fix: resolver bug
docs: actualizar documentación
style: cambios de formato
refactor: refactorizar código
test: agregar tests
chore: actualizar dependencias
```

### Nombre de Ramas

```
feature/descripcion          # Nueva feature
fix/descripcion             # Bug fix
docs/descripcion            # Documentación
refactor/descripcion        # Refactorización
test/descripcion            # Tests
chore/descripcion           # Mantenimiento
```

### Code Style

- **Lenguaje:** Python 3.10+
- **Formatter:** Black
- **Linter:** Flake8
- **Type checker:** Mypy
- **Line length:** 88 caracteres

```python
# ✅ Bien
async def create_booking(
    booking_in: BookingCreate,
    guest_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Booking:
    """Crea una nueva reserva con validaciones."""
    pass


# ❌ Mal
async def create_booking(booking_in, guest_id, session):
    pass
```

### Docstrings

Formato Google:

```python
async def calculate_total_price(
    self,
    session: AsyncSession,
    property_id: int,
    check_in: datetime,
    check_out: datetime,
) -> float:
    """
    Calcula el precio total de una reserva.

    Args:
        session: Sesión de BD asincrónica
        property_id: ID de la propiedad
        check_in: Fecha y hora de entrada
        check_out: Fecha y hora de salida

    Returns:
        float: Precio total en USD

    Raises:
        ValueError: Si check_out <= check_in
    """
    pass
```

## Tipos de Contribuciones

### 🐛 Reportar Bugs

Crear issue con:
- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Versión de Python, SO, etc.

```markdown
### Descripción
Al crear una reserva con 0 huéspedes, no hay validación.

### Pasos para reproducir
1. POST /api/v1/bookings?guest_id=1
2. JSON: {"property_id": 1, "number_of_guests": 0, ...}
3. No hay error

### Esperado
Status 400 con mensaje de error

### Sistema
- OS: Linux
- Python: 3.11
- FastAPI: 0.136.0
```

### ✨ Solicitar Features

```markdown
### Descripción
Agregar sistema de reviews para propiedades.

### Caso de uso
Usuarios quieren calificar su experiencia después de una reserva.

### Solución propuesta
- Nuevo modelo Review en models/
- Endpoints GET/POST/DELETE en routes/reviews.py
- Schema ReviewCreate y ReviewResponse

### Alternativas
- Sistema de stars sin comentarios
```

### 📚 Documentación

- Mejorar README
- Agregar ejemplos
- Traducir documentación
- Crear guías

### 🎨 Mejoras de Código

- Refactorización
- Optimización de performance
- Simplificación de lógica
- Tests adicionales

## Structure de PR

```
## Cambios
- Breve descripción de qué cambió

## Tipos de cambios
- [ ] Bug fix (cambio no breaking que resuelve un issue)
- [ ] Feature nueva (cambio no breaking que agrega funcionalidad)
- [ ] Breaking change (feature que causa cambios incompatibles)
- [ ] Documentación

## Testing
- [ ] Escribí tests para los cambios nuevos
- [ ] Todos los tests pasan localmente
- [ ] Cobertura >= 80%

## Checklist
- [ ] Mi código sigue el estilo del proyecto
- [ ] Actualicé la documentación
- [ ] Agregué docstrings
- [ ] No hay warnings en el código
- [ ] Referencié los issues relacionados

Closes #123
```

## Revisión de PRs

Los PRs serán revisados por:

1. Verificar tests pasen
2. Comprobar cobertura
3. Revisar estilo de código
4. Validar lógica
5. Documentación

## Configuración Local de Desarrollo

```bash
# Clonar y setup
git clone <tu-fork>
cd vibi-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e ".[dev]"

# Pre-commit hooks (opcional pero recomendado)
pip install pre-commit
pre-commit install

# Ahora cada commit auto-ejecuta:
# - black
# - flake8
# - mypy
```

## Herramientas Recomendadas

### IDE
- VS Code (Python extension)
- PyCharm Community Edition

### Extensions
- Pylance (type checking)
- Python (Microsoft)
- Pylint
- Black Formatter

### Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```

## Problemas Comunes

### "ImportError: No module named 'app'"
```bash
# Asegúrate de estar en la raíz del proyecto
cd vibi-backend
# Y que el venv esté activado
source venv/bin/activate
```

### Tests fallan localmente
```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Limpiar caché pytest
pytest --cache-clear

# Ejecutar con verbose
pytest -vv
```

### Merge conflicts

```bash
# Actualizar desde upstream
git fetch upstream
git rebase upstream/main

# Resolver conflictos en el editor
# Luego:
git add .
git rebase --continue
git push -f origin feature/nombre
```

## Documentación de Features Nuevas

Si agregas una feature nueva, documenta:

1. **README.md**: Agregar a sección de características
2. **Docstring**: En el código
3. **Example**: CURL o ejemplo de uso
4. **Test**: Casos de test
5. **ROADMAP.md**: Si afecta futuro

```markdown
## Mi Nueva Feature

### Descripción
...

### Uso
```python
# Ejemplo de código
```

### API
- `POST /api/v1/endpoint` - Crear
- `GET /api/v1/endpoint` - Listar
- etc

### Tests
Ejecutar: `pytest tests/test_feature.py`
```

## Comunidad

- **Issues:** Para bugs y features
- **Discussions:** Para preguntas generales
- **Twitter:** @vibi-api
- **Discord:** [Comunidad Vibi]

---

**¡Gracias por contribuir! 🎉**

Tu contribución hace a Vibi mejor para todos.
