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

    # Server bind + reload, used when running ``python backend/main.py``
    # directly. Override with KRISHIVA_HOST / KRISHIVA_PORT / KRISHIVA_RELOAD.
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False

    # Allowed CORS origins. Defaults to a permissive value for local
    # development; set an explicit list in production.
    cors_origins: list[str] = ["*"]

    # When True, the backend serves the real knowledge engine; if it fails to
    # construct (e.g. missing index) it falls back to the stub so the API still
    # boots. Set KRISHIVA_USE_REAL_ENGINE=0 to force the stub.
    use_real_engine: bool = True


@lru_cache
def get_settings() -> Settings:
    """Return a cached ``Settings`` instance."""

    return Settings()
