"""
Guará Manager - Notification Model
====================================
Internal notification system for users.
"""

import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import TenantScopedModel


class NotificationType(str, enum.Enum):
    """Notification severity/type."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Notification(TenantScopedModel):
    """
    Internal notification for a user.
    Can link to any entity in the system via the link field.
    """

    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType, name="notification_type", create_type=True),
        default=NotificationType.INFO,
        nullable=False,
    )
    link: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="Deep link to related entity"
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False, index=True
    )

    # Relationships
    user = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, title='{self.title}', read={self.is_read})>"
