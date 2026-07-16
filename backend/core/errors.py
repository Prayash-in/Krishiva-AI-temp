"""
Domain exceptions and the exception handlers that turn them into a consistent
JSON error envelope.

No handler ever leaks a stack trace to the client. Server-side, 5xx errors are
logged with their full traceback for debugging.
"""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.schemas.errors import ErrorDetail, ErrorResponse


class EngineError(Exception):
    """The knowledge engine failed to process a query."""

    def __init__(self, message: str = "The knowledge engine failed.") -> None:
        super().__init__(message)
        self.message = message


class EngineTimeoutError(EngineError):
    """The knowledge engine did not respond in time."""

    def __init__(self, message: str = "The knowledge engine timed out.") -> None:
        super().__init__(message)


def _request_id(request: Request) -> str:
    """Return the correlation id set by the request-context middleware."""

    return getattr(request.state, "request_id", "-")


def _error_response(
    request: Request,
    *,
    code: str,
    message: str,
    http_status: int,
) -> JSONResponse:
    """Build a ``JSONResponse`` wrapping the standard error envelope."""

    body = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            request_id=_request_id(request),
        )
    )
    return JSONResponse(status_code=http_status, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the application."""

    @app.exception_handler(RequestValidationError)
    async def _handle_validation(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.warning("Request validation failed: {}", exc.errors())
        return _error_response(
            request,
            code="validation_error",
            message="Request validation failed.",
            http_status=status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    @app.exception_handler(EngineTimeoutError)
    async def _handle_engine_timeout(
        request: Request,
        exc: EngineTimeoutError,
    ) -> JSONResponse:
        logger.error("Engine timeout: {}", exc.message)
        return _error_response(
            request,
            code="engine_timeout",
            message=exc.message,
            http_status=status.HTTP_504_GATEWAY_TIMEOUT,
        )

    @app.exception_handler(EngineError)
    async def _handle_engine_error(
        request: Request,
        exc: EngineError,
    ) -> JSONResponse:
        logger.error("Engine error: {}", exc.message)
        return _error_response(
            request,
            code="engine_error",
            message=exc.message,
            http_status=status.HTTP_502_BAD_GATEWAY,
        )

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http_exception(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        return _error_response(
            request,
            code="http_error",
            message=str(exc.detail),
            http_status=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled exception")
        return _error_response(
            request,
            code="internal_error",
            message="An unexpected error occurred.",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
