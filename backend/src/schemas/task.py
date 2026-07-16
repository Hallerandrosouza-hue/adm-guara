"""
Guará Manager - Task Schemas
==============================
DTOs for task management.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID | None = None
    parent_task_id: UUID | None = None
    assignee_id: UUID | None = None
    status: TaskStatus = TaskStatus.BACKLOG
    priority: TaskPriority = TaskPriority.MEDIUM
    start_date: date | None = None
    due_date: date | None = None
    estimated_hours: float | None = None
    labels: list[str] = Field(default_factory=list)
    custom_fields: dict = Field(default_factory=dict)


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: str | None = None
    description: str | None = None
    project_id: UUID | None = None
    assignee_id: UUID | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    start_date: date | None = None
    due_date: date | None = None
    estimated_hours: float | None = None
    labels: list[str] | None = None
    custom_fields: dict | None = None
    order: int | None = None


class TaskReorder(BaseModel):
    """Schema for reordering tasks (Kanban drag & drop)."""
    task_id: UUID
    new_status: TaskStatus
    new_order: int


class TaskResponse(BaseModel):
    """Full task response DTO."""
    id: UUID
    title: str
    description: str | None
    project_id: UUID | None
    parent_task_id: UUID | None
    assignee_id: UUID | None
    status: TaskStatus
    priority: TaskPriority
    start_date: date | None
    due_date: date | None
    estimated_hours: float | None
    time_spent_hours: float
    order: int
    labels: list[str]
    custom_fields: dict
    created_at: datetime
    updated_at: datetime

    # Nested
    assignee: "TaskUserMinimal | None" = None
    project_name: str | None = None

    model_config = {"from_attributes": True}


class TaskListItem(BaseModel):
    """Compact task for list/kanban views."""
    id: UUID
    title: str
    status: TaskStatus
    priority: TaskPriority
    assignee_id: UUID | None
    due_date: date | None
    order: int
    labels: list[str]
    project_id: UUID | None

    assignee: "TaskUserMinimal | None" = None

    model_config = {"from_attributes": True}


class TaskFilter(BaseModel):
    """Filter options for task listing."""
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: UUID | None = None
    project_id: UUID | None = None
    search: str | None = None
    labels: list[str] | None = None


class TaskUserMinimal(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    avatar_url: str | None
    model_config = {"from_attributes": True}


# Resolve forward references
TaskResponse.model_rebuild()
TaskListItem.model_rebuild()
