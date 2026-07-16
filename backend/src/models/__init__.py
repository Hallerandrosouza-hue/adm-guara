"""
Guará Manager - Models Package
===============================
Imports all models so they are registered with SQLAlchemy's metadata.
This is important for Alembic migration auto-detection.
"""

from src.models.base import Base, BaseModel, TenantScopedModel
from src.models.tenant import Tenant
from src.models.user import User, UserRole, RefreshToken
from src.models.project import (
    Project,
    ProjectStatus,
    ProjectPriority,
    ProjectChecklist,
    ProjectComment,
    ProjectAttachment,
)
from src.models.task import (
    Task,
    TaskStatus,
    TaskPriority,
    TaskDependency,
    TaskChecklist,
    TaskComment,
    TaskAttachment,
    TaskTimeEntry,
)
from src.models.crm import (
    CRMClient,
    PipelineStage,
    ActivityType,
    CRMActivity,
    CRMAttachment,
)
from src.models.notification import Notification, NotificationType

__all__ = [
    "Base",
    "BaseModel",
    "TenantScopedModel",
    "Tenant",
    "User",
    "UserRole",
    "RefreshToken",
    "Project",
    "ProjectStatus",
    "ProjectPriority",
    "ProjectChecklist",
    "ProjectComment",
    "ProjectAttachment",
    "Task",
    "TaskStatus",
    "TaskPriority",
    "TaskDependency",
    "TaskChecklist",
    "TaskComment",
    "TaskAttachment",
    "TaskTimeEntry",
    "CRMClient",
    "PipelineStage",
    "ActivityType",
    "CRMActivity",
    "CRMAttachment",
    "Notification",
    "NotificationType",
]
