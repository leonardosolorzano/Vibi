"""
Rutas de usuarios.

Práctica aplicada: RESTful API Design
- Operaciones CRUD estándar
- Códigos HTTP apropiados
- Validación con schemas Pydantic
- Inyección de dependencias
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from app.services import user_service

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Usuario no encontrado"}},
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Crea un nuevo usuario en la plataforma.

    Args:
        user_in: Datos del usuario a crear
        session: Sesión de BD inyectada

    Returns:
        Usuario creado con su ID

    Raises:
        HTTPException 400: Email ya existe
    """
    # Validar que el email no exista
    existing_user = await user_service.get_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    # Crear usuario
    user_data = user_in.model_dump()
    user_data["password_hash"] = user_service.hash_password(user_data.pop("password"))

    return await user_service.create(session, user_data)


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Listar todos los usuarios",
)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
) -> List[User]:
    """
    Obtiene lista paginada de usuarios.

    Args:
        skip: Número de usuarios a saltar
        limit: Máximo de usuarios a retornar
        session: Sesión de BD inyectada

    Returns:
        Lista de usuarios
    """
    return await user_service.get_all(session, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener detalles de un usuario",
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Obtiene los detalles de un usuario específico.

    Args:
        user_id: ID del usuario
        session: Sesión de BD inyectada

    Returns:
        Detalles del usuario

    Raises:
        HTTPException 404: Usuario no encontrado
    """
    user = await user_service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar un usuario",
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> User:
    """
    Actualiza los datos de un usuario.

    Args:
        user_id: ID del usuario a actualizar
        user_in: Nuevos datos
        session: Sesión de BD inyectada

    Returns:
        Usuario actualizado

    Raises:
        HTTPException 404: Usuario no encontrado
    """
    user = await user_service.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )

    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = user_service.hash_password(
            update_data.pop("password")
        )

    return await user_service.update(session, user, update_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> None:
    """
    Elimina un usuario de la plataforma.

    Args:
        user_id: ID del usuario a eliminar
        session: Sesión de BD inyectada

    Raises:
        HTTPException 404: Usuario no encontrado
    """
    success = await user_service.delete(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
