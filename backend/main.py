"""
Application factory and ASGI entrypoint.

``create_app`` wires configuration, logging, middleware, routers and exception
handlers into a ready-to-serve FastAPI application. The module-level ``app`` is
what ``uvicorn backend.main:app`` serves.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.api.routes import health_router, query_router
from backend.core.config import Settings, get_settings
from backend.core.errors import register_exception_handlers
from backend.core.logging import configure_logging
from backend.core.middleware import RequestContextMiddleware
from backend.engine_gateway.stub import StubQueryEngine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Construct shared resources once per process.

    The engine is instantiated here so it is created a single time and shared
    across requests. Swap ``StubQueryEngine`` for the real engine when ready.
    """

    settings = get_settings()

    app.state.engine = StubQueryEngine()

    logger.info(
        "{} started (env={}, version={})",
        settings.app_name,
        settings.environment,
        settings.version,
    )

    yield

    logger.info("{} shutting down", settings.app_name)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build and configure the FastAPI application."""

    settings = settings or get_settings()
    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        lifespan=lifespan,
    )

    # Request-context (id + logging) is inner; CORS is outermost so its headers
    # apply to every response, including errors.
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(health_router)
    app.include_router(query_router, prefix=settings.api_prefix)

    return app


app = create_app()
