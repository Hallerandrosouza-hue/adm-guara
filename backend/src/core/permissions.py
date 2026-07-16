"""
Guará Manager - Permission System
===================================
RBAC permission matrix mapping roles to granular permissions.
"""

import enum
from src.models.user import UserRole


class Permission(str, enum.Enum):
    """Granular permissions for the system."""

    # Dashboard
    DASHBOARD_VIEW = "dashboard:view"

    # Projects
    PROJECTS_VIEW = "projects:view"
    PROJECTS_CREATE = "projects:create"
    PROJECTS_EDIT = "projects:edit"
    PROJECTS_DELETE = "projects:delete"
    PROJECTS_MANAGE_ALL = "projects:manage_all"

    # Tasks
    TASKS_VIEW = "tasks:view"
    TASKS_CREATE = "tasks:create"
    TASKS_EDIT = "tasks:edit"
    TASKS_DELETE = "tasks:delete"
    TASKS_MANAGE_ALL = "tasks:manage_all"

    # CRM
    CRM_VIEW = "crm:view"
    CRM_CREATE = "crm:create"
    CRM_EDIT = "crm:edit"
    CRM_DELETE = "crm:delete"
    CRM_MANAGE_ALL = "crm:manage_all"

    # Financial
    FINANCIAL_VIEW = "financial:view"
    FINANCIAL_CREATE = "financial:create"
    FINANCIAL_EDIT = "financial:edit"
    FINANCIAL_DELETE = "financial:delete"

    # HR
    HR_VIEW = "hr:view"
    HR_CREATE = "hr:create"
    HR_EDIT = "hr:edit"
    HR_DELETE = "hr:delete"

    # Users
    USERS_VIEW = "users:view"
    USERS_CREATE = "users:create"
    USERS_EDIT = "users:edit"
    USERS_DELETE = "users:delete"

    # Settings
    SETTINGS_VIEW = "settings:view"
    SETTINGS_EDIT = "settings:edit"

    # Documents
    DOCUMENTS_VIEW = "documents:view"
    DOCUMENTS_CREATE = "documents:create"
    DOCUMENTS_EDIT = "documents:edit"
    DOCUMENTS_DELETE = "documents:delete"

    # Reports
    REPORTS_VIEW = "reports:view"
    REPORTS_EXPORT = "reports:export"

    # Notifications
    NOTIFICATIONS_VIEW = "notifications:view"
    NOTIFICATIONS_MANAGE = "notifications:manage"


# Role-Permission mapping matrix
# Each role maps to a set of allowed permissions
ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.ADMIN: set(Permission),  # Admin has ALL permissions

    UserRole.DIRECTOR: {
        Permission.DASHBOARD_VIEW,
        Permission.PROJECTS_VIEW, Permission.PROJECTS_CREATE,
        Permission.PROJECTS_EDIT, Permission.PROJECTS_DELETE, Permission.PROJECTS_MANAGE_ALL,
        Permission.TASKS_VIEW, Permission.TASKS_CREATE,
        Permission.TASKS_EDIT, Permission.TASKS_DELETE, Permission.TASKS_MANAGE_ALL,
        Permission.CRM_VIEW, Permission.CRM_CREATE,
        Permission.CRM_EDIT, Permission.CRM_DELETE, Permission.CRM_MANAGE_ALL,
        Permission.FINANCIAL_VIEW, Permission.FINANCIAL_CREATE,
        Permission.FINANCIAL_EDIT, Permission.FINANCIAL_DELETE,
        Permission.HR_VIEW, Permission.HR_CREATE, Permission.HR_EDIT, Permission.HR_DELETE,
        Permission.USERS_VIEW, Permission.USERS_CREATE, Permission.USERS_EDIT,
        Permission.SETTINGS_VIEW, Permission.SETTINGS_EDIT,
        Permission.DOCUMENTS_VIEW, Permission.DOCUMENTS_CREATE,
        Permission.DOCUMENTS_EDIT, Permission.DOCUMENTS_DELETE,
        Permission.REPORTS_VIEW, Permission.REPORTS_EXPORT,
        Permission.NOTIFICATIONS_VIEW, Permission.NOTIFICATIONS_MANAGE,
    },

    UserRole.MANAGER: {
        Permission.DASHBOARD_VIEW,
        Permission.PROJECTS_VIEW, Permission.PROJECTS_CREATE,
        Permission.PROJECTS_EDIT, Permission.PROJECTS_MANAGE_ALL,
        Permission.TASKS_VIEW, Permission.TASKS_CREATE,
        Permission.TASKS_EDIT, Permission.TASKS_DELETE, Permission.TASKS_MANAGE_ALL,
        Permission.CRM_VIEW, Permission.CRM_CREATE, Permission.CRM_EDIT,
        Permission.USERS_VIEW,
        Permission.DOCUMENTS_VIEW, Permission.DOCUMENTS_CREATE, Permission.DOCUMENTS_EDIT,
        Permission.REPORTS_VIEW, Permission.REPORTS_EXPORT,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.FINANCIAL: {
        Permission.DASHBOARD_VIEW,
        Permission.FINANCIAL_VIEW, Permission.FINANCIAL_CREATE,
        Permission.FINANCIAL_EDIT, Permission.FINANCIAL_DELETE,
        Permission.PROJECTS_VIEW,
        Permission.CRM_VIEW,
        Permission.REPORTS_VIEW, Permission.REPORTS_EXPORT,
        Permission.DOCUMENTS_VIEW,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.HR: {
        Permission.DASHBOARD_VIEW,
        Permission.HR_VIEW, Permission.HR_CREATE, Permission.HR_EDIT, Permission.HR_DELETE,
        Permission.USERS_VIEW, Permission.USERS_CREATE, Permission.USERS_EDIT,
        Permission.DOCUMENTS_VIEW, Permission.DOCUMENTS_CREATE,
        Permission.REPORTS_VIEW,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.MARKETING: {
        Permission.DASHBOARD_VIEW,
        Permission.CRM_VIEW, Permission.CRM_CREATE, Permission.CRM_EDIT,
        Permission.PROJECTS_VIEW,
        Permission.TASKS_VIEW, Permission.TASKS_CREATE, Permission.TASKS_EDIT,
        Permission.DOCUMENTS_VIEW, Permission.DOCUMENTS_CREATE,
        Permission.REPORTS_VIEW,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.DEVELOPER: {
        Permission.DASHBOARD_VIEW,
        Permission.PROJECTS_VIEW,
        Permission.TASKS_VIEW, Permission.TASKS_CREATE, Permission.TASKS_EDIT,
        Permission.DOCUMENTS_VIEW, Permission.DOCUMENTS_CREATE,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.COMMERCIAL: {
        Permission.DASHBOARD_VIEW,
        Permission.CRM_VIEW, Permission.CRM_CREATE,
        Permission.CRM_EDIT, Permission.CRM_MANAGE_ALL,
        Permission.PROJECTS_VIEW,
        Permission.TASKS_VIEW, Permission.TASKS_CREATE,
        Permission.DOCUMENTS_VIEW,
        Permission.REPORTS_VIEW,
        Permission.NOTIFICATIONS_VIEW,
    },

    UserRole.CLIENT: {
        Permission.PROJECTS_VIEW,
        Permission.TASKS_VIEW,
        Permission.DOCUMENTS_VIEW,
        Permission.NOTIFICATIONS_VIEW,
    },
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission."""
    return permission in ROLE_PERMISSIONS.get(role, set())


def get_permissions(role: UserRole) -> set[Permission]:
    """Get all permissions for a role."""
    return ROLE_PERMISSIONS.get(role, set())
