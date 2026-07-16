"""
Guará Manager - FastAPI Dependencies
======================================
Authentication and authorization dependencies for route injection.
"""

import uuid
from typing import Annotated

from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ForbiddenError, UnauthorizedError
from src.core.permissions import Permission, has_permission
from src.core.security import verify_token
from src.database import get_db
from src.models.user import User

# Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    FastAPI dependency that extracts and validates the current user from JWT.
    
    Raises:
        UnauthorizedError: If token is missing, invalid, or user not found.
    """
    if not credentials:
        raise UnauthorizedError("Authentication required")

    payload = verify_token(credentials.credentials, expected_type="access")
    if not payload:
        raise UnauthorizedError("Invalid or expired access token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise UnauthorizedError("Invalid token payload")

    result = await db.execute(
        select(User).where(User.id == user_uuid, User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise UnauthorizedError("User account is deactivated")

    return user


async def get_current_tenant_id(
    current_user: Annotated[User, Depends(get_current_user)],
) -> uuid.UUID:
    """Extract tenant_id from the current authenticated user."""
    return current_user.tenant_id


def require_permissions(*permissions: Permission):
    """
    Factory that creates a dependency requiring specific permissions.
    
    Usage:
        @router.get("/", dependencies=[Depends(require_permissions(Permission.PROJECTS_VIEW))])
    
    Args:
        *permissions: One or more permissions required. User must have ALL of them.
    """

    async def _check_permissions(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        for perm in permissions:
            if not has_permission(current_user.role, perm):
                raise ForbiddenError(
                    f"Permission '{perm.value}' required. "
                    f"Your role '{current_user.role.value}' does not have this permission."
                )
        return current_user

    return _check_permissions
