"""
Guará Manager - Dashboard Service
===================================
Business logic for dashboard statistics.
"""

from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.project import Project, ProjectStatus
from src.models.crm import CRMClient, PipelineStage
from src.models.user import User

class DashboardService:
    async def get_stats(self, db: AsyncSession, tenant_id: UUID):
        """Aggregate data for dashboard KPI cards."""
        
        # Active Projects
        stmt_proj = select(func.count(Project.id)).where(
            Project.tenant_id == tenant_id,
            Project.status.in_([ProjectStatus.IN_PROGRESS, ProjectStatus.NOT_STARTED]),
            Project.is_deleted == False
        )
        res_proj = await db.execute(stmt_proj)
        active_projects = res_proj.scalar_one()

        # Total Leads
        stmt_leads = select(func.count(CRMClient.id)).where(
            CRMClient.tenant_id == tenant_id,
            CRMClient.pipeline_stage == PipelineStage.LEAD,
            CRMClient.is_deleted == False
        )
        res_leads = await db.execute(stmt_leads)
        total_leads = res_leads.scalar_one()

        # Active Employees (Users)
        stmt_users = select(func.count(User.id)).where(
            User.tenant_id == tenant_id,
            User.is_active == True,
            User.is_deleted == False
        )
        res_users = await db.execute(stmt_users)
        active_users = res_users.scalar_one()

        # Mock Revenue for now (will be implemented in Phase 2 with Financial module)
        return {
            "revenue": 125000.00,
            "expenses": 45000.00,
            "profit": 80000.00,
            "active_projects": active_projects,
            "total_leads": total_leads,
            "active_users": active_users
        }

dashboard_service = DashboardService()
