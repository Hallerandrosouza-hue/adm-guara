"""
Guará Manager - User Model
===========================
User entity with role-based access control (RBAC).
Users are always scoped to a tenant.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import TenantScopedModel, BaseModel


class UserRole(str, enum.Enum):
    """RBAC roles for the system."""
    ADMIN = "admin"
    DIRECTOR = "director"
    MANAGER = "manager"
    FINANCIAL = "financial"
    HR = "hr"
    MARKETING = "marketing"
    DEVELOPER = "developer"
    COMMERCIAL = "commercial"
    CLIENT = "client"


class User(TenantScopedModel):
    """
    User entity scoped to a tenant.
    Email is unique within a tenant (not globally).
    """

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
    )

    # Authentication
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Role & Status
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", create_type=True),
        default=UserRole.DEVELOPER,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true", nullable=False
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="users", lazy="selectin")
    refresh_tokens = relationship(
        "RefreshToken", back_populates="user", lazy="noload", cascade="all, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        """User's full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"


class RefreshToken(BaseModel):
    """
    Stores refresh tokens for JWT authentication.
    Tokens can be revoked individually for security.
    """

    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="refresh_tokens", lazy="selectin")

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
