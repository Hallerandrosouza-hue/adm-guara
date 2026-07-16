"""
Guará Manager - Auth Routes
============================
Endpoints for authentication and registration.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user
from src.database import get_db
from src.models.user import User
from src.schemas.auth import AuthUserResponse, LoginRequest, RegisterRequest, TokenResponse
from src.services.auth_service import auth_service

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(
    request: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Register a new tenant and admin user."""
    return await auth_service.register(db, request)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Authenticate user and return tokens."""
    return await auth_service.login(db, request)


@router.get("/me", response_model=AuthUserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Get current authenticated user info."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role.value,
        "avatar_url": current_user.avatar_url,
        "tenant_id": current_user.tenant_id,
        "tenant_name": current_user.tenant.name if hasattr(current_user, "tenant") else ""
    }
