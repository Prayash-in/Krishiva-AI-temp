"""
Application factory and ASGI entrypoint.

``create_app`` wires configuration, logging, middleware, routers and exception
handlers into a ready-to-serve FastAPI application. The module-level ``app`` is
what ``uvicorn backend.main:app`` serves.
"""

from __future__ import annotations

# When executed directly (``python backend/main.py``), Python puts ``backend/``
# on ``sys.path`` instead of the project root, so the absolute ``backend.*``
# imports below fail. Prepend the project root before those imports run. (Under
# uvicorn/`create_app` the package is already importable, so this is a no-op.)
if __name__ == "__main__":
    import sys
    from pathlib import Path

    _project_root = str(Path(__file__).resolve().parents[1])
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

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
from backend.engine_gateway.contract import QueryEngine
from backend.engine_gateway.stub import StubQueryEngine


def _build_engine(settings: Settings) -> QueryEngine:
    """Construct the query engine, falling back to the stub on failure.

    The real engine loads an embedding model and opens the vector store, which
    can fail (missing index, missing model download). We never let that take
    down the API: on any error we log it and serve the deterministic stub so
    the frontend still has a working endpoint.
    """

    if not settings.use_real_engine:
        logger.info("KRISHIVA_USE_REAL_ENGINE=0 — serving the stub engine.")
        return StubQueryEngine()

    try:
        # Imported here so a broken engine dependency can't stop the module
        # from importing; the stub remains available as a fallback.
        from backend.engine_gateway.krishiva_adapter import KrishivaQueryEngine

        engine = KrishivaQueryEngine.build()
        logger.info("Knowledge engine ready.")
        return engine
    except Exception as exc:  # noqa: BLE001 - degrade gracefully to the stub
        logger.exception("Failed to build the knowledge engine: {}", exc)
        logger.warning("Falling back to the stub engine.")
        return StubQueryEngine()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Construct shared resources once per process.

    The engine is instantiated here so it is created a single time and shared
    across requests.
    """

    settings = get_settings()

    app.state.engine = _build_engine(settings)

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


def _run() -> None:
    """Run the app with uvicorn when this module is executed directly.

    The project root is placed on ``sys.path`` at import time (see the top of
    this module), so the ``backend.*`` import string resolves here too.
    """

    import uvicorn

    settings = get_settings()
    # Pass the import string (not the ``app`` object) so ``reload`` works.
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    _run()
