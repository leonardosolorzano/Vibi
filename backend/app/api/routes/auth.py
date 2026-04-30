"""
Rutas de autenticación.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.schemas import UserResponse
from app.services import user_service

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=255)


@router.post(
    "/login",
    response_model=UserResponse,
    summary="Iniciar sesión",
)
async def login(
    payload: LoginInput,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Valida credenciales y retorna el usuario.
    """
    user = await user_service.get_by_email(session, payload.email)
    if not user or not user_service.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user
