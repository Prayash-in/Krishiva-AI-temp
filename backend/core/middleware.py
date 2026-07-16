"""
Request-context middleware.

Assigns a correlation id to every request, binds it to the logger for the
duration of the request, logs the request/response with latency, and echoes
the id back in the ``X-Request-ID`` response header.
"""

from __future__ import annotations

import time
import uuid
from collections.abc import Awaitable, Callable

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_REQUEST_ID_HEADER = "X-Request-ID"


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach a request id and structured request/response logging."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get(_REQUEST_ID_HEADER) or uuid.uuid4().hex
        request.state.request_id = request_id

        start = time.perf_counter()

        with logger.contextualize(request_id=request_id):
            logger.info("--> {} {}", request.method, request.url.path)

            response = await call_next(request)

            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info(
                "<-- {} {} {} ({:.1f} ms)",
                request.method,
                request.url.path,
                response.status_code,
                elapsed_ms,
            )

        response.headers[_REQUEST_ID_HEADER] = request_id
        return response
