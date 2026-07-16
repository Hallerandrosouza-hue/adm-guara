"""
Guará Manager - Project Model
==============================
Project entity with checklist, comments, and attachments.
"""

import enum
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import TenantScopedModel


class ProjectStatus(str, enum.Enum):
    """Project lifecycle status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectPriority(str, enum.Enum):
    """Project priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Project(TenantScopedModel):
    """
    Project entity representing a managed project.
    Contains tasks, checklists, comments, and attachments.
    """

    __tablename__ = "projects"

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Client association (from CRM)
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crm_clients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Responsible user
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Financial
    budget: Mapped[float | None] = mapped_column(
        Numeric(12, 2), nullable=True, comment="Project budget in BRL"
    )

    # Timeline
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Status & Progress
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status", create_type=True),
        default=ProjectStatus.NOT_STARTED,
        nullable=False,
        index=True,
    )
    priority: Mapped[ProjectPriority] = mapped_column(
        Enum(ProjectPriority, name="project_priority", create_type=True),
        default=ProjectPriority.MEDIUM,
        nullable=False,
    )
    progress_percent: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )
    total_hours_worked: Mapped[float] = mapped_column(
        Float, default=0.0, server_default="0", nullable=False
    )

    # Relationships
    responsible = relationship("User", foreign_keys=[responsible_id], lazy="selectin")
    client = relationship("CRMClient", foreign_keys=[client_id], lazy="selectin")
    tasks = relationship("Task", back_populates="project", lazy="noload")
    checklists = relationship(
        "ProjectChecklist", back_populates="project", lazy="noload", cascade="all, delete-orphan"
    )
    comments = relationship(
        "ProjectComment", back_populates="project", lazy="noload", cascade="all, delete-orphan"
    )
    attachments = relationship(
        "ProjectAttachment", back_populates="project", lazy="noload", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status.value}')>"


class ProjectChecklist(TenantScopedModel):
    """Checklist item within a project."""

    __tablename__ = "project_checklists"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)

    # Relationships
    project = relationship("Project", back_populates="checklists")


class ProjectComment(TenantScopedModel):
    """Comment on a project."""

    __tablename__ = "project_comments"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="comments")
    user = relationship("User", lazy="selectin")


class ProjectAttachment(TenantScopedModel):
    """File attachment on a project."""

    __tablename__ = "project_attachments"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    project = relationship("Project", back_populates="attachments")
