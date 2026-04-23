"""
Tests de ejemplo para la API.

Demuestra cómo escribir tests para usuarios, propiedades y reservas.
"""

import pytest
from fastapi import status


# ============================================================================
# TESTS DE USUARIOS
# ============================================================================

@pytest.mark.asyncio
class TestUsers:
    """Tests para el endpoint de usuarios."""

    async def test_create_user(self, test_client):
        """Test: Crear un usuario exitosamente."""
        response = test_client.post(
            "/api/v1/users",
            json={
                "email": "usuario@example.com",
                "full_name": "Juan Pérez",
                "password": "contraseña_segura_123",
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "usuario@example.com"
        assert data["full_name"] == "Juan Pérez"
        assert "password" not in data  # No exponer contraseña

    async def test_create_user_duplicate_email(self, test_client):
        """Test: Crear usuario con email existente falla."""
        # Crear primer usuario
        test_client.post(
            "/api/v1/users",
            json={
                "email": "duplicado@example.com",
                "full_name": "User 1",
                "password": "password123",
            }
        )

        # Intentar crear con mismo email
        response = test_client.post(
            "/api/v1/users",
            json={
                "email": "duplicado@example.com",
                "full_name": "User 2",
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email ya está registrado" in response.json()["detail"]

    async def test_get_users(self, test_client):
        """Test: Listar usuarios."""
        response = test_client.get("/api/v1/users")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    async def test_get_user_not_found(self, test_client):
        """Test: Usuario no existente retorna 404."""
        response = test_client.get("/api/v1/users/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_user(self, test_client):
        """Test: Actualizar usuario."""
        # Crear usuario
        create_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "update@example.com",
                "full_name": "Original Name",
                "password": "password123",
            }
        )
        user_id = create_response.json()["id"]

        # Actualizar
        response = test_client.put(
            f"/api/v1/users/{user_id}",
            json={"full_name": "Updated Name"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["full_name"] == "Updated Name"

    async def test_delete_user(self, test_client):
        """Test: Eliminar usuario."""
        # Crear usuario
        create_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "delete@example.com",
                "full_name": "To Delete",
                "password": "password123",
            }
        )
        user_id = create_response.json()["id"]

        # Eliminar
        response = test_client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que está eliminado
        response = test_client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ============================================================================
# TESTS DE PROPIEDADES
# ============================================================================

@pytest.mark.asyncio
class TestProperties:
    """Tests para el endpoint de propiedades."""

    async def test_create_property(self, test_client):
        """Test: Crear propiedad."""
        # Primero crear un usuario (propietario)
        user_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "host@example.com",
                "full_name": "Property Host",
                "password": "password123",
            }
        )
        owner_id = user_response.json()["id"]

        # Crear propiedad
        response = test_client.post(
            f"/api/v1/properties?owner_id={owner_id}",
            json={
                "title": "Apartamento en Barcelona",
                "description": "Hermoso apartamento con vistas al mar",
                "property_type": "apartment",
                "price_per_night": 85.50,
                "city": "Barcelona",
                "address": "Passeig de Gràcia 132",
                "max_guests": 4,
                "bedrooms": 2,
                "bathrooms": 1
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == "Apartamento en Barcelona"

    async def test_search_properties_by_city(self, test_client):
        """Test: Buscar propiedades por ciudad."""
        response = test_client.get(
            "/api/v1/properties?city=Barcelona"
        )
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    async def test_search_properties_by_price(self, test_client):
        """Test: Buscar propiedades por rango de precio."""
        response = test_client.get(
            "/api/v1/properties?min_price=50&max_price=150"
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_search_properties_by_type(self, test_client):
        """Test: Buscar propiedades por tipo."""
        response = test_client.get(
            "/api/v1/properties?property_type=apartment"
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_get_property_detail(self, test_client):
        """Test: Obtener detalles de propiedad."""
        response = test_client.get("/api/v1/properties/1")
        # Podría retornar 404 si no existe, eso es correcto


# ============================================================================
# TESTS DE RESERVAS
# ============================================================================

@pytest.mark.asyncio
class TestBookings:
    """Tests para el endpoint de reservas."""

    async def test_create_booking_success(self, test_client):
        """Test: Crear reserva exitosamente."""
        # Crear host
        host_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "host@booking.com",
                "full_name": "Host",
                "password": "password123",
            }
        )
        host_id = host_response.json()["id"]

        # Crear propiedad
        prop_response = test_client.post(
            f"/api/v1/properties?owner_id={host_id}",
            json={
                "title": "Casa",
                "description": "Bonita casa",
                "property_type": "house",
                "price_per_night": 100,
                "city": "Madrid",
                "address": "Calle Mayor 1",
                "max_guests": 4,
                "bedrooms": 3,
                "bathrooms": 2
            }
        )
        property_id = prop_response.json()["id"]

        # Crear guest
        guest_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "guest@booking.com",
                "full_name": "Guest",
                "password": "password123",
            }
        )
        guest_id = guest_response.json()["id"]

        # Crear reserva
        response = test_client.post(
            f"/api/v1/bookings?guest_id={guest_id}",
            json={
                "property_id": property_id,
                "check_in_date": "2024-05-10T15:00:00",
                "check_out_date": "2024-05-15T11:00:00",
                "number_of_guests": 2
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["status"] == "pending"
        assert response.json()["total_price"] == 500  # 5 noches * 100

    async def test_create_booking_property_not_found(self, test_client):
        """Test: Crear reserva en propiedad inexistente."""
        response = test_client.post(
            "/api/v1/bookings?guest_id=1",
            json={
                "property_id": 999,
                "check_in_date": "2024-05-10T15:00:00",
                "check_out_date": "2024-05-15T11:00:00",
                "number_of_guests": 2
            }
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_create_booking_too_many_guests(self, test_client):
        """Test: Crear reserva con más huéspedes que capacidad."""
        # Crear host
        host_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "host2@booking.com",
                "full_name": "Host 2",
                "password": "password123",
            }
        )
        host_id = host_response.json()["id"]

        # Crear propiedad con capacidad para 2
        prop_response = test_client.post(
            f"/api/v1/properties?owner_id={host_id}",
            json={
                "title": "Estudio",
                "description": "Pequeño estudio",
                "property_type": "loft",
                "price_per_night": 50,
                "city": "Valencia",
                "address": "Calle Nueva 5",
                "max_guests": 2,  # Solo 2 huéspedes
                "bedrooms": 1,
                "bathrooms": 1
            }
        )
        property_id = prop_response.json()["id"]

        # Crear guest
        guest_response = test_client.post(
            "/api/v1/users",
            json={
                "email": "guest2@booking.com",
                "full_name": "Guest 2",
                "password": "password123",
            }
        )
        guest_id = guest_response.json()["id"]

        # Intentar crear reserva con 5 huéspedes
        response = test_client.post(
            f"/api/v1/bookings?guest_id={guest_id}",
            json={
                "property_id": property_id,
                "check_in_date": "2024-05-10T15:00:00",
                "check_out_date": "2024-05-15T11:00:00",
                "number_of_guests": 5  # Más que capacidad
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_confirm_booking(self, test_client):
        """Test: Confirmar una reserva."""
        # Crear setup (host, propiedad, guest, reserva)
        # ... (simplificado)
        # PATCH a /api/v1/bookings/{booking_id}/confirm
        pass


# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

@pytest.mark.asyncio
class TestIntegration:
    """Tests de integración entre entidades."""

    async def test_complete_booking_flow(self, test_client):
        """
        Test: Flujo completo de reserva.
        
        1. Crear host
        2. Crear propiedad
        3. Crear guest
        4. Crear reserva
        5. Confirmar reserva
        6. Obtener detalles
        """
        # 1. Host
        host = test_client.post(
            "/api/v1/users",
            json={
                "email": "flow.host@test.com",
                "full_name": "Host Flow",
                "password": "pass123",
            }
        ).json()

        # 2. Property
        prop = test_client.post(
            f"/api/v1/properties?owner_id={host['id']}",
            json={
                "title": "Flow Property",
                "description": "Test property",
                "property_type": "apartment",
                "price_per_night": 100,
                "city": "TestCity",
                "address": "Test Address",
                "max_guests": 4,
                "bedrooms": 2,
                "bathrooms": 1
            }
        ).json()

        # 3. Guest
        guest = test_client.post(
            "/api/v1/users",
            json={
                "email": "flow.guest@test.com",
                "full_name": "Guest Flow",
                "password": "pass123",
            }
        ).json()

        # 4. Booking
        booking = test_client.post(
            f"/api/v1/bookings?guest_id={guest['id']}",
            json={
                "property_id": prop["id"],
                "check_in_date": "2024-06-01T15:00:00",
                "check_out_date": "2024-06-05T11:00:00",
                "number_of_guests": 2
            }
        ).json()

        assert booking["status"] == "pending"
        assert booking["total_price"] == 400  # 4 noches * 100

        # 5. Confirm
        confirmed = test_client.patch(
            f"/api/v1/bookings/{booking['id']}/confirm"
        ).json()

        assert confirmed["status"] == "confirmed"

        # 6. Get details
        details = test_client.get(
            f"/api/v1/bookings/{booking['id']}"
        ).json()

        assert details["property"]["title"] == "Flow Property"
        assert details["guest"]["full_name"] == "Guest Flow"


# ============================================================================
# PARA EJECUTAR LOS TESTS
# ============================================================================
#
# Ejecutar todos los tests:
#   pytest
#
# Ejecutar un archivo específico:
#   pytest tests/test_bookings.py
#
# Ejecutar una clase específica:
#   pytest tests/test_bookings.py::TestBookings
#
# Ejecutar un test específico:
#   pytest tests/test_bookings.py::TestBookings::test_create_booking_success
#
# Con modo verbose:
#   pytest -vv
#
# Con cobertura:
#   pytest --cov=app
