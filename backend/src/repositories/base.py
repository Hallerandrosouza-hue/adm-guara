"""
Guará Manager - Base Repository
================================
Generic repository pattern for data access.
"""

from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic repository providing standard CRUD operations."""

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: UUID, tenant_id: UUID | None = None) -> ModelType | None:
        """Get a single record by ID. If tenant_id is provided, filters by it."""
        stmt = select(self.model).where(self.model.id == id, getattr(self.model, "is_deleted", False) == False)
        
        if tenant_id and hasattr(self.model, "tenant_id"):
            stmt = stmt.where(self.model.tenant_id == tenant_id)
            
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
        self,
        db: AsyncSession,
        tenant_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
        **filters
    ) -> tuple[list[ModelType], int]:
        """List records with basic filtering and pagination."""
        stmt = select(self.model).where(getattr(self.model, "is_deleted", False) == False)
        
        if tenant_id and hasattr(self.model, "tenant_id"):
            stmt = stmt.where(self.model.tenant_id == tenant_id)
            
        for key, value in filters.items():
            if value is not None and hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)

        # Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        # Get items
        stmt = stmt.offset(skip).limit(limit)
        
        # We assume standard ordering by created_at desc if available
        if hasattr(self.model, "created_at"):
            stmt = stmt.order_by(self.model.created_at.desc())
            
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        
        return items, total

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType | dict[str, Any], tenant_id: UUID | None = None) -> ModelType:
        """Create a new record."""
        obj_in_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        
        if tenant_id and hasattr(self.model, "tenant_id"):
            obj_in_data["tenant_id"] = tenant_id
            
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in: UpdateSchemaType | dict[str, Any]) -> ModelType:
        """Update an existing record."""
        obj_data = {
            c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns
        }
        update_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: UUID, tenant_id: UUID | None = None) -> ModelType | None:
        """Soft delete a record."""
        obj = await self.get_by_id(db=db, id=id, tenant_id=tenant_id)
        if obj and hasattr(obj, "is_deleted"):
            obj.is_deleted = True
            obj.deleted_at = func.now()
            db.add(obj)
            await db.flush()
        return obj
