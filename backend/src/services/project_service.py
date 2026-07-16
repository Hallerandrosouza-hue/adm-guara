"""
Guará Manager - Project Service
================================
Business logic for projects.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.project_repository import project_repo
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.models.project import Project


class ProjectService:
    async def get_projects(self, db: AsyncSession, tenant_id: UUID, **filters):
        return await project_repo.list_with_filters(db, tenant_id, **filters)
        
    async def get_project(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> Project | None:
        return await project_repo.get_by_id(db, id, tenant_id)
        
    async def create_project(self, db: AsyncSession, tenant_id: UUID, data: ProjectCreate) -> Project:
        return await project_repo.create(db, obj_in=data, tenant_id=tenant_id)
        
    async def update_project(self, db: AsyncSession, id: UUID, tenant_id: UUID, data: ProjectUpdate) -> Project | None:
        project = await project_repo.get_by_id(db, id, tenant_id)
        if not project:
            return None
        return await project_repo.update(db, db_obj=project, obj_in=data)
        
    async def delete_project(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> bool:
        project = await project_repo.delete(db, id=id, tenant_id=tenant_id)
        return project is not None

project_service = ProjectService()
