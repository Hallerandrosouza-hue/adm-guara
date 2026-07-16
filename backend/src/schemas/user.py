"""
Guará Manager - User Schemas
==============================
DTOs for user management.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for creating a new user within a tenant."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = None
    role: UserRole = UserRole.DEVELOPER


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    """User response DTO."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    full_name: str
    avatar_url: str | None
    phone: str | None
    role: UserRole
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListItem(BaseModel):
    """Compact user representation for lists."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    full_name: str
    avatar_url: str | None
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}
