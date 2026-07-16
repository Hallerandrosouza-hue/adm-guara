"""
Guará Manager - Users Routes
=============================
Endpoints for user management within a tenant.
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
from src.schemas.user import UserCreate, UserListItem, UserResponse, UserUpdate
from src.repositories.user_repository import user_repo

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserListItem], dependencies=[Depends(require_permissions(Permission.USERS_VIEW))])
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
    pagination: Annotated[PaginationParams, Depends()],
):
    """List users for the current tenant."""
    items, total = await user_repo.list(
        db,
        tenant_id=tenant_id,
        skip=pagination.offset,
        limit=pagination.page_size
    )
    return PaginatedResponse.create(items, total, pagination.page, pagination.page_size)

# Detailed endpoints (create, update, delete, get) omitted for brevity in Phase 1,
# but structure follows projects/tasks
