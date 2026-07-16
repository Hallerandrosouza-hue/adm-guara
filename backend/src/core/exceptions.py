"""
Guará Manager - Custom Exceptions
===================================
Application-specific exceptions with HTTP status code mapping.
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundError(AppException):
    """Resource not found (404)."""

    def __init__(self, resource: str = "Resource", identifier: str = ""):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} '{identifier}' not found"
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ForbiddenError(AppException):
    """Access forbidden (403)."""

    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class UnauthorizedError(AppException):
    """Authentication required (401)."""

    def __init__(self, detail: str = "Invalid or expired credentials"):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ConflictError(AppException):
    """Resource conflict (409)."""

    def __init__(self, detail: str = "Resource already exists"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class ValidationError(AppException):
    """Validation error (422)."""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class RateLimitError(AppException):
    """Rate limit exceeded (429)."""

    def __init__(self, detail: str = "Rate limit exceeded. Please try again later."):
        super().__init__(
            detail=detail, status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
