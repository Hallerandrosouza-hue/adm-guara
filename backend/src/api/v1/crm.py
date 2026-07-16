"""
Guará Manager - CRM Routes
===========================
Endpoints for CRM client management.
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
from src.schemas.crm import (
    CRMClientCreate,
    CRMClientFilter,
    CRMClientListItem,
    CRMClientResponse,
    CRMClientUpdate,
    CRMPipelineReorder,
)
from src.services.crm_service import crm_service

router = APIRouter()


@router.get("/clients", response_model=PaginatedResponse[CRMClientListItem], dependencies=[Depends(require_permissions(Permission.CRM_VIEW))])
async def list_clients(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    filters: Annotated[CRMClientFilter, Depends()],
    pagination: Annotated[PaginationParams, Depends()],
):
    """List CRM clients/leads for the current tenant."""
    items, total = await crm_service.get_clients(
        db,
        tenant_id,
        skip=pagination.offset,
        limit=pagination.page_size,
        **filters.model_dump(exclude_unset=True)
    )
    return PaginatedResponse.create(items, total, pagination.page, pagination.page_size)


@router.post("/clients", response_model=CRMClientResponse, dependencies=[Depends(require_permissions(Permission.CRM_CREATE))])
async def create_client(
    data: CRMClientCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Create a new CRM client/lead."""
    return await crm_service.create_client(db, tenant_id, data)


@router.get("/clients/{id}", response_model=CRMClientResponse, dependencies=[Depends(require_permissions(Permission.CRM_VIEW))])
async def get_client(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Get a CRM client by ID."""
    client = await crm_service.get_client(db, id, tenant_id)
    if not client:
        raise NotFoundError("Client", str(id))
    return client


@router.put("/clients/{id}", response_model=CRMClientResponse, dependencies=[Depends(require_permissions(Permission.CRM_EDIT))])
async def update_client(
    id: UUID,
    data: CRMClientUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Update a CRM client."""
    client = await crm_service.update_client(db, id, tenant_id, data)
    if not client:
        raise NotFoundError("Client", str(id))
    return client

@router.post("/clients/reorder", response_model=CRMClientResponse, dependencies=[Depends(require_permissions(Permission.CRM_EDIT))])
async def reorder_client(
    data: CRMPipelineReorder,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Reorder CRM client (for Pipeline drag & drop)."""
    client = await crm_service.reorder_client(db, tenant_id, data)
    if not client:
         raise NotFoundError("Client", str(data.client_id))
    return client

@router.delete("/clients/{id}", dependencies=[Depends(require_permissions(Permission.CRM_DELETE))])
async def delete_client(
    id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Soft delete a CRM client."""
    success = await crm_service.delete_client(db, id, tenant_id)
    if not success:
        raise NotFoundError("Client", str(id))
    return {"message": "Client deleted successfully", "success": True}
