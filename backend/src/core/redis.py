"""
Guará Manager - Redis Client
==============================
Async Redis client singleton with cache helpers.
"""

import json
from typing import Any

from redis.asyncio import Redis

from src.config import get_settings

settings = get_settings()

# Global redis client instance
_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """Get or create the Redis client singleton."""
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(
            settings.redis_url,
            decode_responses=True,
            max_connections=20,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection on shutdown."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


async def get_cached(key: str) -> Any | None:
    """
    Get a cached value from Redis.
    Returns None if key doesn't exist.
    """
    redis = await get_redis()
    value = await redis.get(key)
    if value:
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return None


async def set_cached(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """
    Set a cached value in Redis with TTL.
    
    Args:
        key: Cache key.
        value: Value to cache (will be JSON serialized).
        ttl_seconds: Time-to-live in seconds (default: 5 minutes).
    """
    redis = await get_redis()
    serialized = json.dumps(value, default=str)
    await redis.setex(key, ttl_seconds, serialized)


async def invalidate(pattern: str) -> None:
    """
    Invalidate all cached keys matching a pattern.
    
    Args:
        pattern: Redis key pattern (e.g., 'tenant:*:projects').
    """
    redis = await get_redis()
    async for key in redis.scan_iter(match=pattern):
        await redis.delete(key)
