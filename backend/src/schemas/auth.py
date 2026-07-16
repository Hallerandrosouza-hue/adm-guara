"""
Guará Manager - Auth Schemas
==============================
DTOs for authentication endpoints.
"""

from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request payload."""
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    """Registration request — creates a new tenant + admin user."""
    # Tenant info
    company_name: str = Field(min_length=2, max_length=255)
    company_slug: str = Field(
        min_length=2, max_length=100, pattern=r"^[a-z0-9\-]+$",
        description="URL-friendly company identifier (lowercase, hyphens)"
    )
    # User info
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    """JWT token pair response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Access token expiry in seconds")


class RefreshRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class AuthUserResponse(BaseModel):
    """Authenticated user info returned after login."""
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: str
    avatar_url: str | None
    tenant_id: UUID
    tenant_name: str

    model_config = {"from_attributes": True}
