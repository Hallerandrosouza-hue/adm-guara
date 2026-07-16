"""
Guará Manager - Project Routes
===============================
Endpoints for project management.
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
from src.schemas.project import (
    ProjectCreate,
    ProjectFilter,
    ProjectListItem,
    ProjectResponse,
    ProjectUpdate,
)
from src.services.project_service import project_service

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ProjectListItem], dependencies=[Depends(require_permissions(Permission.PROJECTS_VIEW))])
async def list_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    filters: Annotated[ProjectFilter, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
):
    """List projects for the current tenant."""
    items, total = await project_service.get_projects(
        db,
        tenant_id,
        skip=pagination.offset,
        limit=pagination.page_size,
        **filters.model_dump(exclude_unset=True)
    )
    return PaginatedResponse.create(items, total, pagination.page, pagination.page_size)


@router.post("", response_model=ProjectResponse, dependencies=[Depends(require_permissions(Permission.PROJECTS_CREATE))])
async def create_project(
    data: ProjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Create a new project."""
    return await project_service.create_project(db, tenant_id, data)


@router.get("/{id}", response_model=ProjectResponse, dependencies=[Depends(require_permissions(Permission.PROJECTS_VIEW))])
async def get_project(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Get a project by ID."""
    project = await project_service.get_project(db, id, tenant_id)
    if not project:
        raise NotFoundError("Project", str(id))
    return project


@router.put("/{id}", response_model=ProjectResponse, dependencies=[Depends(require_permissions(Permission.PROJECTS_EDIT))])
async def update_project(
    id: UUID,
    data: ProjectUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Update a project."""
    project = await project_service.update_project(db, id, tenant_id, data)
    if not project:
        raise NotFoundError("Project", str(id))
    return project


@router.delete("/{id}", dependencies=[Depends(require_permissions(Permission.PROJECTS_DELETE))])
async def delete_project(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Soft delete a project."""
    success = await project_service.delete_project(db, id, tenant_id)
    if not success:
        raise NotFoundError("Project", str(id))
    return {"message": "Project deleted successfully", "success": True}
