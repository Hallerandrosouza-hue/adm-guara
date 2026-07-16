"""
Guará Manager - Task Model
===========================
Task entity with subtasks, dependencies, time tracking,
checklists, comments, and attachments.
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
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import TenantScopedModel


class TaskStatus(str, enum.Enum):
    """Task status for Kanban board columns."""
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class TaskPriority(str, enum.Enum):
    """Task priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(TenantScopedModel):
    """
    Task entity supporting Kanban, list, calendar, and timeline views.
    Supports subtasks via self-referential parent_task_id.
    """

    __tablename__ = "tasks"

    # Basic info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Project association
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Subtask support (self-referential)
    parent_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Assignment
    assignee_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Status & Priority
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, name="task_status", create_type=True),
        default=TaskStatus.BACKLOG,
        nullable=False,
        index=True,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority, name="task_priority", create_type=True),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )

    # Timeline
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Time tracking
    estimated_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    time_spent_hours: Mapped[float] = mapped_column(
        Float, default=0.0, server_default="0", nullable=False
    )

    # Kanban ordering
    order: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )

    # Flexible fields
    labels: Mapped[list] = mapped_column(
        JSONB, default=list, server_default="[]", nullable=False,
        comment="Array of label strings for tagging"
    )
    custom_fields: Mapped[dict] = mapped_column(
        JSONB, default=dict, server_default="{}", nullable=False,
        comment="User-defined custom fields"
    )

    # Relationships
    project = relationship("Project", back_populates="tasks", lazy="selectin")
    assignee = relationship("User", foreign_keys=[assignee_id], lazy="selectin")
    parent_task = relationship("Task", remote_side="Task.id", lazy="noload")
    subtasks = relationship("Task", back_populates="parent_task", lazy="noload")
    dependencies = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        lazy="noload",
        cascade="all, delete-orphan",
    )
    checklists = relationship(
        "TaskChecklist", back_populates="task", lazy="noload", cascade="all, delete-orphan"
    )
    comments = relationship(
        "TaskComment", back_populates="task", lazy="noload", cascade="all, delete-orphan"
    )
    attachments = relationship(
        "TaskAttachment", back_populates="task", lazy="noload", cascade="all, delete-orphan"
    )
    time_entries = relationship(
        "TaskTimeEntry", back_populates="task", lazy="noload", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status.value}')>"


class TaskDependency(TenantScopedModel):
    """Dependency between tasks (task depends on depends_on)."""

    __tablename__ = "task_dependencies"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    depends_on_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")
    depends_on = relationship("Task", foreign_keys=[depends_on_id], lazy="selectin")


class TaskChecklist(TenantScopedModel):
    """Checklist item within a task."""

    __tablename__ = "task_checklists"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false", nullable=False
    )
    order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)

    # Relationships
    task = relationship("Task", back_populates="checklists")


class TaskComment(TenantScopedModel):
    """Comment on a task."""

    __tablename__ = "task_comments"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
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
    task = relationship("Task", back_populates="comments")
    user = relationship("User", lazy="selectin")


class TaskAttachment(TenantScopedModel):
    """File attachment on a task."""

    __tablename__ = "task_attachments"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    task = relationship("Task", back_populates="attachments")


class TaskTimeEntry(TenantScopedModel):
    """Time tracking entry for a task."""

    __tablename__ = "task_time_entries"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    task = relationship("Task", back_populates="time_entries")
    user = relationship("User", lazy="selectin")
