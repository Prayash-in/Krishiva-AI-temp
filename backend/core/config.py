"""
Application configuration.

Settings are loaded from environment variables (optionally via a ``.env``
file) using ``pydantic-settings``. No secrets are hardcoded here.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the backend.

    Every field can be overridden with an environment variable prefixed by
    ``KRISHIVA_`` (e.g. ``KRISHIVA_LOG_LEVEL=DEBUG``).
    """

    model_config = SettingsConfigDict(
        env_prefix="KRISHIVA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Krishiva AI"
    version: str = "0.1.0"
    environment: str = "development"

    log_level: str = "INFO"

    api_prefix: str = "/api/v1"

    # Allowed CORS origins. Defaults to a permissive value for local
    # development; set an explicit list in production.
    cors_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance."""

    return Settings()
