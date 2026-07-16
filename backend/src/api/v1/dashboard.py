"""
Guará Manager - Dashboard Routes
=================================
Endpoints for dashboard statistics.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_tenant_id, require_permissions
from src.core.permissions import Permission
from src.database import get_db
from src.services.dashboard_service import dashboard_service

router = APIRouter()


@router.get("/stats", dependencies=[Depends(require_permissions(Permission.DASHBOARD_VIEW))])
async def get_dashboard_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    tenant_id: Annotated[UUID, Depends(get_current_tenant_id)],
):
    """Get aggregated statistics for the dashboard."""
    return await dashboard_service.get_stats(db, tenant_id)
