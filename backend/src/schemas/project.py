"""
Guará Manager - Project Schemas
=================================
DTOs for project management.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.models.project import ProjectPriority, ProjectStatus


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    category: str | None = None
    client_id: UUID | None = None
    responsible_id: UUID | None = None
    budget: float | None = None
    start_date: date | None = None
    deadline: date | None = None
    status: ProjectStatus = ProjectStatus.NOT_STARTED
    priority: ProjectPriority = ProjectPriority.MEDIUM


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: str | None = None
    description: str | None = None
    category: str | None = None
    client_id: UUID | None = None
    responsible_id: UUID | None = None
    budget: float | None = None
    start_date: date | None = None
    deadline: date | None = None
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None
    progress_percent: int | None = Field(default=None, ge=0, le=100)


class ProjectResponse(BaseModel):
    """Full project response DTO."""
    id: UUID
    name: str
    description: str | None
    category: str | None
    client_id: UUID | None
    responsible_id: UUID | None
    budget: float | None
    start_date: date | None
    deadline: date | None
    status: ProjectStatus
    priority: ProjectPriority
    progress_percent: int
    total_hours_worked: float
    created_at: datetime
    updated_at: datetime

    # Nested
    responsible: "UserMinimal | None" = None
    client: "ClientMinimal | None" = None

    model_config = {"from_attributes": True}


class ProjectListItem(BaseModel):
    """Compact project for list views."""
    id: UUID
    name: str
    status: ProjectStatus
    priority: ProjectPriority
    progress_percent: int
    deadline: date | None
    responsible_id: UUID | None
    budget: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectFilter(BaseModel):
    """Filter options for project listing."""
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None
    responsible_id: UUID | None = None
    category: str | None = None
    search: str | None = None


# Minimal nested schemas to avoid circular imports
class UserMinimal(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    avatar_url: str | None
    model_config = {"from_attributes": True}


class ClientMinimal(BaseModel):
    id: UUID
    contact_name: str
    company_name: str | None
    model_config = {"from_attributes": True}


# Resolve forward references
ProjectResponse.model_rebuild()
