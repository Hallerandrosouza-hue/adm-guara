"""
Guará Manager - Task Service
=============================
Business logic for tasks.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.task_repository import task_repo
from src.schemas.task import TaskCreate, TaskUpdate, TaskReorder
from src.models.task import Task


class TaskService:
    async def get_tasks(self, db: AsyncSession, tenant_id: UUID, **filters):
        return await task_repo.list_with_filters(db, tenant_id, **filters)
        
    async def get_task(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> Task | None:
        return await task_repo.get_by_id(db, id, tenant_id)
        
    async def create_task(self, db: AsyncSession, tenant_id: UUID, data: TaskCreate) -> Task:
        return await task_repo.create(db, obj_in=data, tenant_id=tenant_id)
        
    async def update_task(self, db: AsyncSession, id: UUID, tenant_id: UUID, data: TaskUpdate) -> Task | None:
        task = await task_repo.get_by_id(db, id, tenant_id)
        if not task:
            return None
        return await task_repo.update(db, db_obj=task, obj_in=data)
        
    async def delete_task(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> bool:
        task = await task_repo.delete(db, id=id, tenant_id=tenant_id)
        return task is not None
        
    async def reorder_task(self, db: AsyncSession, tenant_id: UUID, data: TaskReorder) -> Task | None:
        """Update a task's status and order for Kanban drag-and-drop."""
        task = await task_repo.get_by_id(db, data.task_id, tenant_id)
        if not task:
            return None
            
        task.status = data.new_status
        task.order = data.new_order
        
        # Optional: Rebalance orders of other tasks in the column
        
        db.add(task)
        await db.flush()
        return task

task_service = TaskService()
