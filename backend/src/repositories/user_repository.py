"""
Guará Manager - User Repository
================================
Data access layer for User entity.
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.repositories.base import BaseRepository
from src.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User specific database operations."""

    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str, tenant_id: UUID | None = None) -> User | None:
        """Get active user by email."""
        stmt = select(User).where(User.email == email, User.is_deleted == False)
        if tenant_id:
            stmt = stmt.where(User.tenant_id == tenant_id)
        
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

user_repo = UserRepository()
