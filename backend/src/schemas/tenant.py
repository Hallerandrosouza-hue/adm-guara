"""
Guará Manager - Tenant Schemas
================================
DTOs for tenant management.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    """Schema for creating a new tenant."""
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9\-]+$")
    logo_url: str | None = None
    description: str | None = None


class TenantUpdate(BaseModel):
    """Schema for updating a tenant."""
    name: str | None = None
    logo_url: str | None = None
    description: str | None = None
    settings: dict | None = None


class TenantResponse(BaseModel):
    """Tenant response DTO."""
    id: UUID
    name: str
    slug: str
    logo_url: str | None
    description: str | None
    plan: str
    is_active: bool
    settings: dict
    created_at: datetime

    model_config = {"from_attributes": True}
