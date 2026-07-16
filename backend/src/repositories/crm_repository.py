"""
Guará Manager - CRM Repository
===============================
Data access layer for CRMClient entity.
"""

from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.crm import CRMClient
from src.repositories.base import BaseRepository
from src.schemas.crm import CRMClientCreate, CRMClientUpdate


class CRMRepository(BaseRepository[CRMClient, CRMClientCreate, CRMClientUpdate]):
    """CRM specific database operations."""

    def __init__(self):
        super().__init__(CRMClient)

    async def list_with_filters(
        self,
        db: AsyncSession,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        pipeline_stage: str | None = None,
        responsible_id: UUID | None = None,
        search: str | None = None,
    ):
        stmt = select(self.model).where(
            self.model.tenant_id == tenant_id,
            self.model.is_deleted == False
        )
        
        if pipeline_stage:
            stmt = stmt.where(self.model.pipeline_stage == pipeline_stage)
            
        if responsible_id:
            stmt = stmt.where(self.model.responsible_id == responsible_id)
            
        if search:
            stmt = stmt.where(
                or_(
                    self.model.contact_name.ilike(f"%{search}%"),
                    self.model.company_name.ilike(f"%{search}%"),
                    self.model.email.ilike(f"%{search}%"),
                )
            )

        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        stmt = stmt.order_by(self.model.order.asc(), self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

crm_repo = CRMRepository()
