"""
Guará Manager - Project Repository
===================================
Data access layer for Project entity.
"""

from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.project import Project
from src.repositories.base import BaseRepository
from src.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    """Project specific database operations."""

    def __init__(self):
        super().__init__(Project)

    async def list_with_filters(
        self,
        db: AsyncSession,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        status: str | None = None,
        priority: str | None = None,
        responsible_id: UUID | None = None
    ):
        """List projects with advanced filtering."""
        stmt = select(self.model).where(
            self.model.tenant_id == tenant_id,
            self.model.is_deleted == False
        )
        
        if search:
            stmt = stmt.where(
                or_(
                    self.model.name.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%")
                )
            )
            
        if status:
            stmt = stmt.where(self.model.status == status)
            
        if priority:
            stmt = stmt.where(self.model.priority == priority)
            
        if responsible_id:
            stmt = stmt.where(self.model.responsible_id == responsible_id)

        # Execute count and items similarly to base repo, but custom for specific needs if necessary
        # We can leverage the base repo's logic or implement here
        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        stmt = stmt.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

project_repo = ProjectRepository()
