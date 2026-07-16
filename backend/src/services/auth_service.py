"""
Guará Manager - Auth Service
=============================
Business logic for authentication and registration.
"""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import ConflictError, UnauthorizedError
from src.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from src.models.tenant import Tenant
from src.models.user import RefreshToken, UserRole
from src.repositories.user_repository import user_repo
from src.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    """Service handling authentication flows."""

    async def register(self, db: AsyncSession, request: RegisterRequest) -> TokenResponse:
        """Register a new tenant and an admin user, and log them in."""
        # 1. Check if slug exists
        stmt_slug = select(Tenant).where(Tenant.slug == request.company_slug)
        res_slug = await db.execute(stmt_slug)
        if res_slug.scalar_one_or_none():
            raise ConflictError("Company URL slug already taken")

        # 2. Create Tenant
        tenant = Tenant(
            name=request.company_name,
            slug=request.company_slug,
        )
        db.add(tenant)
        await db.flush()  # To get tenant.id

        # 3. Create Admin User
        admin_user = await user_repo.create(
            db,
            obj_in={
                "email": request.email,
                "password_hash": hash_password(request.password),
                "first_name": request.first_name,
                "last_name": request.last_name,
                "role": UserRole.ADMIN,
            },
            tenant_id=tenant.id,
        )

        return await self._generate_tokens(db, admin_user, tenant.name)

    async def login(self, db: AsyncSession, request: LoginRequest) -> TokenResponse:
        """Authenticate a user and return tokens."""
        # Note: We query without tenant_id first to find the user globally by email
        # In a real multi-tenant scenario with shared emails across tenants, 
        # login usually requires the tenant slug first. Here we assume unique email globally for simplicity 
        # or that they login through a tenant-specific URL.
        # For this MVP, we just find the user by email.
        stmt = select(User).where(User.email == request.email, User.is_deleted == False)
        from src.models.user import User
        res = await db.execute(stmt)
        user = res.scalar_one_or_none()

        if not user or not verify_password(request.password, user.password_hash):
            raise UnauthorizedError("Incorrect email or password")
            
        if not user.is_active:
             raise UnauthorizedError("User account is disabled")

        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        
        # Get tenant info for token payload
        await db.refresh(user, ["tenant"])

        return await self._generate_tokens(db, user, user.tenant.name)

    async def _generate_tokens(self, db: AsyncSession, user, tenant_name: str) -> TokenResponse:
        """Generate access and refresh tokens, store refresh token."""
        from src.config import get_settings
        settings = get_settings()
        
        access_payload = {
            "sub": str(user.id),
            "tenant_id": str(user.tenant_id),
            "tenant_name": tenant_name,
            "role": user.role.value,
        }
        access_token = create_access_token(access_payload)

        refresh_payload = {
            "sub": str(user.id),
        }
        refresh_token = create_refresh_token(refresh_payload)

        # Store refresh token in DB
        # Optional: Delete old ones
        rt = RefreshToken(
            user_id=user.id,
            token_hash=hash_password(refresh_token),  # Hash it for security
            expires_at=datetime.now(timezone.utc) + __import__("datetime").timedelta(days=settings.jwt_refresh_token_expire_days)
        )
        db.add(rt)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.jwt_access_token_expire_minutes * 60
        )

auth_service = AuthService()
