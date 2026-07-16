"""
Guará Manager - Tenant Model
=============================
Represents a company/organization in the multi-tenant system.
Each tenant has completely isolated data.
"""

import uuid

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel


class Tenant(BaseModel):
    """
    Tenant represents a company/organization.
    All data in the system is scoped to a tenant.
    """

    __tablename__ = "tenants"

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Subscription
    plan: Mapped[str] = mapped_column(
        String(50), default="free", server_default="free", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )

    # Settings stored as JSONB for flexibility
    settings: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        server_default="{}",
        nullable=False,
        comment="Tenant settings: timezone, language, currency, theme, etc.",
    )

    # Relationships
    users = relationship("User", back_populates="tenant", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Tenant(id={self.id}, name='{self.name}', slug='{self.slug}')>"
