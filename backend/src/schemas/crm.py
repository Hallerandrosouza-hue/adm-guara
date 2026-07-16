"""
Guará Manager - CRM Schemas
==============================
DTOs for CRM management.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from src.models.crm import ActivityType, PipelineStage


class CRMClientCreate(BaseModel):
    """Schema for creating a new CRM client/lead."""
    company_name: str | None = None
    contact_name: str = Field(min_length=1, max_length=255)
    phone: str | None = None
    whatsapp: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    cnpj: str | None = None
    segment: str | None = None
    origin: str | None = None
    potential_value: float | None = None
    responsible_id: UUID | None = None
    pipeline_stage: PipelineStage = PipelineStage.LEAD
    notes: str | None = None
    tags: list[str] = Field(default_factory=list)


class CRMClientUpdate(BaseModel):
    """Schema for updating a CRM client."""
    company_name: str | None = None
    contact_name: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    email: EmailStr | None = None
    website: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    cnpj: str | None = None
    segment: str | None = None
    origin: str | None = None
    potential_value: float | None = None
    responsible_id: UUID | None = None
    pipeline_stage: PipelineStage | None = None
    notes: str | None = None
    tags: list[str] | None = None
    order: int | None = None


class CRMClientResponse(BaseModel):
    """Full CRM client response DTO."""
    id: UUID
    company_name: str | None
    contact_name: str
    phone: str | None
    whatsapp: str | None
    email: str | None
    website: str | None
    address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    cnpj: str | None
    segment: str | None
    origin: str | None
    potential_value: float | None
    responsible_id: UUID | None
    pipeline_stage: PipelineStage
    notes: str | None
    tags: list[str]
    order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CRMClientListItem(BaseModel):
    """Compact CRM client for pipeline/list views."""
    id: UUID
    company_name: str | None
    contact_name: str
    email: str | None
    phone: str | None
    potential_value: float | None
    pipeline_stage: PipelineStage
    responsible_id: UUID | None
    order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CRMPipelineReorder(BaseModel):
    """Schema for reordering clients in the pipeline (drag & drop)."""
    client_id: UUID
    new_stage: PipelineStage
    new_order: int


class CRMClientFilter(BaseModel):
    """Filter options for CRM client listing."""
    pipeline_stage: PipelineStage | None = None
    responsible_id: UUID | None = None
    segment: str | None = None
    origin: str | None = None
    search: str | None = None


class CRMActivityCreate(BaseModel):
    """Schema for creating a CRM activity."""
    client_id: UUID
    activity_type: ActivityType
    description: str = Field(min_length=1)
    scheduled_at: datetime | None = None


class CRMActivityResponse(BaseModel):
    """CRM activity response DTO."""
    id: UUID
    client_id: UUID
    user_id: UUID
    activity_type: ActivityType
    description: str
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
