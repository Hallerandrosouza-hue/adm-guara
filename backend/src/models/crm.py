"""
Guará Manager - CRM Model
==========================
Client/Lead entity with pipeline stages, activities, and attachments.
"""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import TenantScopedModel


class PipelineStage(str, enum.Enum):
    """CRM pipeline stages for lead/client progression."""
    LEAD = "lead"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class ActivityType(str, enum.Enum):
    """Types of CRM activities."""
    CALL = "call"
    EMAIL = "email"
    MEETING = "meeting"
    NOTE = "note"
    WHATSAPP = "whatsapp"
    VISIT = "visit"


class CRMClient(TenantScopedModel):
    """
    CRM Client/Lead entity.
    Progresses through pipeline stages from Lead to Won/Lost.
    """

    __tablename__ = "crm_clients"

    # Company info
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Contact info
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Address
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True)
    zip_code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # Business info
    cnpj: Mapped[str | None] = mapped_column(String(18), nullable=True)
    segment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    origin: Mapped[str | None] = mapped_column(String(100), nullable=True)
    potential_value: Mapped[float | None] = mapped_column(
        Numeric(12, 2), nullable=True, comment="Potential deal value in BRL"
    )

    # Pipeline
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    pipeline_stage: Mapped[PipelineStage] = mapped_column(
        Enum(PipelineStage, name="pipeline_stage", create_type=True),
        default=PipelineStage.LEAD,
        nullable=False,
        index=True,
    )

    # Flexible fields
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list] = mapped_column(
        JSONB, default=list, server_default="[]", nullable=False
    )

    # Kanban ordering
    order: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0", nullable=False
    )

    # Relationships
    responsible = relationship("User", foreign_keys=[responsible_id], lazy="selectin")
    activities = relationship(
        "CRMActivity", back_populates="client", lazy="noload", cascade="all, delete-orphan"
    )
    attachments = relationship(
        "CRMAttachment", back_populates="client", lazy="noload", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<CRMClient(id={self.id}, name='{self.contact_name}', "
            f"stage='{self.pipeline_stage.value}')>"
        )


class CRMActivity(TenantScopedModel):
    """Activity log for a CRM client (calls, emails, meetings, etc.)."""

    __tablename__ = "crm_activities"

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crm_clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    activity_type: Mapped[ActivityType] = mapped_column(
        Enum(ActivityType, name="activity_type", create_type=True),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    client = relationship("CRMClient", back_populates="activities")
    user = relationship("User", lazy="selectin")


class CRMAttachment(TenantScopedModel):
    """File attachment on a CRM client."""

    __tablename__ = "crm_attachments"

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crm_clients.id", ondelete="CASCADE"),
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
    client = relationship("CRMClient", back_populates="attachments")
