"""
Guará Manager - Task Repository
================================
Data access layer for Task entity.
"""

from uuid import UUID

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.repositories.base import BaseRepository
from src.schemas.task import TaskCreate, TaskUpdate


class TaskRepository(BaseRepository[Task, TaskCreate, TaskUpdate]):
    """Task specific database operations."""

    def __init__(self):
        super().__init__(Task)

    async def list_with_filters(
        self,
        db: AsyncSession,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 100,
        project_id: UUID | None = None,
        assignee_id: UUID | None = None,
        status: str | None = None,
        priority: str | None = None,
        search: str | None = None,
    ):
        stmt = select(self.model).where(
            self.model.tenant_id == tenant_id,
            self.model.is_deleted == False
        )
        
        if project_id:
            stmt = stmt.where(self.model.project_id == project_id)
            
        if assignee_id:
            stmt = stmt.where(self.model.assignee_id == assignee_id)
            
        if status:
            stmt = stmt.where(self.model.status == status)
            
        if priority:
            stmt = stmt.where(self.model.priority == priority)
            
        if search:
            stmt = stmt.where(
                or_(
                    self.model.title.ilike(f"%{search}%"),
                    self.model.description.ilike(f"%{search}%")
                )
            )

        from sqlalchemy import func
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # Order by Kanban 'order' field first, then creation date
        stmt = stmt.order_by(self.model.order.asc(), self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

task_repo = TaskRepository()
