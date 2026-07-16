"""
HTTP routes.

- ``GET  /health``        — liveness probe (unversioned).
- ``POST /api/v1/query``  — answer a farmer query (mounted under the API prefix).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from backend.api.deps import get_query_service
from backend.core.config import get_settings
from backend.schemas.errors import ErrorResponse
from backend.schemas.query import QueryRequest, QueryResponse
from backend.services.query_service import QueryService

health_router = APIRouter(tags=["health"])


@health_router.get("/health")
def health() -> dict[str, str]:
    """Return a simple liveness payload."""

    settings = get_settings()
    return {"status": "ok", "version": settings.version}


query_router = APIRouter(tags=["query"])


@query_router.post(
    "/query",
    response_model=QueryResponse,
    responses={
        422: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        504: {"model": ErrorResponse},
    },
)
def create_query(
    payload: QueryRequest,
    request: Request,
    service: QueryService = Depends(get_query_service),
) -> QueryResponse:
    """Answer a farmer query and return a structured response."""

    return service.handle(payload, request.state.request_id)
