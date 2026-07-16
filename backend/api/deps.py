"""
FastAPI dependency providers.

The engine is constructed once at startup and stored on ``app.state``; these
providers expose it (and the service wrapping it) to route handlers.
"""

from __future__ import annotations

from fastapi import Depends, Request

from backend.engine_gateway.contract import QueryEngine
from backend.services.query_service import QueryService


def get_engine(request: Request) -> QueryEngine:
    """Return the process-wide engine instance."""

    return request.app.state.engine


def get_query_service(
    engine: QueryEngine = Depends(get_engine),
) -> QueryService:
    """Return a :class:`QueryService` bound to the current engine."""

    return QueryService(engine)
