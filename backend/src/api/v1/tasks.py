"""
Guará Manager - Task Routes
============================
Endpoints for task management.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_tenant_id, require_permissions
from src.core.exceptions import NotFoundError
from src.core.permissions import Permission
from src.database import get_db
from src.schemas.common import PaginatedResponse, PaginationParams
from src.schemas.task import (
    TaskCreate,
    TaskFilter,
    TaskListItem,
    TaskResponse,
    TaskUpdate,
    TaskReorder,
)
from src.services.task_service import task_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse[TaskListItem], dependencies=[Depends(require_permissions(Permission.TASKS_VIEW))])
async def list_tasks(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    filters: Annotated[TaskFilter, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
):
    """List tasks for the current tenant."""
    items, total = await task_service.get_tasks(
        db,
        tenant_id,
        skip=pagination.offset,
        limit=pagination.page_size,
        **filters.model_dump(exclude_unset=True)
    )
    return PaginatedResponse.create(items, total, pagination.page, pagination.page_size)


@router.post("", response_model=TaskResponse, dependencies=[Depends(require_permissions(Permission.TASKS_CREATE))])
async def create_task(
    data: TaskCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Create a new task."""
    return await task_service.create_task(db, tenant_id, data)


@router.get("/{id}", response_model=TaskResponse, dependencies=[Depends(require_permissions(Permission.TASKS_VIEW))])
async def get_task(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Get a task by ID."""
    task = await task_service.get_task(db, id, tenant_id)
    if not task:
        raise NotFoundError("Task", str(id))
    return task


@router.put("/{id}", response_model=TaskResponse, dependencies=[Depends(require_permissions(Permission.TASKS_EDIT))])
async def update_task(
    id: UUID,
    data: TaskUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Update a task."""
    task = await task_service.update_task(db, id, tenant_id, data)
    if not task:
        raise NotFoundError("Task", str(id))
    return task

@router.post("/reorder", response_model=TaskResponse, dependencies=[Depends(require_permissions(Permission.TASKS_EDIT))])
async def reorder_task(
    data: TaskReorder,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Reorder task (for Kanban drag & drop)."""
    task = await task_service.reorder_task(db, tenant_id, data)
    if not task:
         raise NotFoundError("Task", str(data.task_id))
    return task

@router.delete("/{id}", dependencies=[Depends(require_permissions(Permission.TASKS_DELETE))])
async def delete_task(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Soft delete a task."""
    success = await task_service.delete_task(db, id, tenant_id)
    if not success:
        raise NotFoundError("Task", str(id))
    return {"message": "Task deleted successfully", "success": True}
