"""
Guará Manager - Middleware
===========================
Request-level middleware for logging, rate limiting, and tenant context.
"""

import logging
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("guara")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs request method, path, status code, and duration."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        response: Response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "%s %s → %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        # Add timing header for debugging
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Redis-backed rate limiting per IP address.
    Limits requests to `rate_limit_per_minute` per minute.
    """

    def __init__(self, app, rate_limit: int = 100):
        super().__init__(app)
        self.rate_limit = rate_limit

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ("/health", "/docs", "/openapi.json"):
            return await call_next(request)

        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        try:
            from src.core.redis import get_redis

            redis = await get_redis()
            key = f"rate_limit:{client_ip}"
            current = await redis.incr(key)
            if current == 1:
                await redis.expire(key, 60)  # 1-minute window

            if current > self.rate_limit:
                from src.core.exceptions import RateLimitError
                raise RateLimitError()
        except ImportError:
            pass  # Redis not available, skip rate limiting
        except Exception:
            pass  # Don't break the app if Redis is down

        return await call_next(request)
