"""
Guará Manager - CRM Service
============================
Business logic for CRM clients.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.crm_repository import crm_repo
from src.schemas.crm import CRMClientCreate, CRMClientUpdate, CRMPipelineReorder
from src.models.crm import CRMClient


class CRMService:
    async def get_clients(self, db: AsyncSession, tenant_id: UUID, **filters):
        return await crm_repo.list_with_filters(db, tenant_id, **filters)
        
    async def get_client(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> CRMClient | None:
        return await crm_repo.get_by_id(db, id, tenant_id)
        
    async def create_client(self, db: AsyncSession, tenant_id: UUID, data: CRMClientCreate) -> CRMClient:
        return await crm_repo.create(db, obj_in=data, tenant_id=tenant_id)
        
    async def update_client(self, db: AsyncSession, id: UUID, tenant_id: UUID, data: CRMClientUpdate) -> CRMClient | None:
        client = await crm_repo.get_by_id(db, id, tenant_id)
        if not client:
            return None
        return await crm_repo.update(db, db_obj=client, obj_in=data)
        
    async def delete_client(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> bool:
        client = await crm_repo.delete(db, id=id, tenant_id=tenant_id)
        return client is not None
        
    async def reorder_client(self, db: AsyncSession, tenant_id: UUID, data: CRMPipelineReorder) -> CRMClient | None:
        client = await crm_repo.get_by_id(db, data.client_id, tenant_id)
        if not client:
            return None
            
        client.pipeline_stage = data.new_stage
        client.order = data.new_order
        
        db.add(client)
        await db.flush()
        return client

crm_service = CRMService()
