"""
Guará Manager - Application Configuration
==========================================
Centralized configuration using pydantic-settings.
All values are loaded from environment variables with sensible defaults.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---- Application ----
    app_name: str = "Guará Manager"
    app_env: str = "development"
    app_debug: bool = True

    # ---- Database ----
    postgres_user: str = "guara"
    postgres_password: str = "guara_secret_2024"
    postgres_db: str = "guara_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        """Async PostgreSQL connection string for SQLAlchemy."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_url_sync(self) -> str:
        """Sync PostgreSQL connection string for Alembic migrations."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # ---- Redis ----
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_url: str = "redis://localhost:6379/0"

    # ---- JWT Authentication ----
    jwt_secret_key: str = "change-this-to-a-very-long-random-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # ---- S3 / MinIO ----
    s3_endpoint: str = "http://localhost:9000"
    s3_access_key: str = "guara_minio"
    s3_secret_key: str = "guara_minio_secret"
    s3_bucket_name: str = "guara-uploads"
    s3_region: str = "us-east-1"

    # ---- CORS ----
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    # ---- Rate Limiting ----
    rate_limit_per_minute: int = 100


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
