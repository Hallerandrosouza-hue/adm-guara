"""
Guará Manager - API v1 Router
==============================
Aggregates all API v1 endpoints.
"""

from fastapi import APIRouter

from src.api.v1 import auth, crm, dashboard, projects, tasks, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(crm.router, prefix="/crm", tags=["CRM"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
