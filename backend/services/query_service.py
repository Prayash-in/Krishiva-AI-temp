"""
The query service.

Maps a validated HTTP :class:`QueryRequest` onto the engine boundary, invokes
the engine facade, and maps the :class:`EngineResult` back to the HTTP
:class:`QueryResponse`. Any unexpected engine failure is normalised to
:class:`EngineError` so the API returns a clean 502 rather than a 500.
"""

from __future__ import annotations

from loguru import logger

from backend.core.errors import EngineError
from backend.engine_gateway.contract import (
    EngineRequest,
    EngineResult,
    QueryEngine,
)
from backend.schemas.query import (
    Diagnosis,
    QueryRequest,
    QueryResponse,
    Source,
)


class QueryService:
    """Orchestrates a single farmer-query request against the engine."""

    def __init__(self, engine: QueryEngine) -> None:
        self._engine = engine

    def handle(self, request: QueryRequest, request_id: str) -> QueryResponse:
        """Answer a query and return the structured HTTP response.

        Raises:
            EngineError: if the engine fails (mapped to HTTP 502 upstream).
            EngineTimeoutError: if the engine times out (mapped to HTTP 504).
        """

        engine_request = EngineRequest(
            query=request.query,
            language=request.language,
            region=request.region,
            crop=request.crop,
        )

        logger.info("Dispatching query to engine")

        try:
            result = self._engine.answer(engine_request)
        except EngineError:
            # Already a domain error (incl. EngineTimeoutError) — let it flow.
            raise
        except Exception as exc:  # noqa: BLE001 - normalise to a domain error
            logger.exception("Engine raised an unexpected error")
            raise EngineError(
                "The knowledge engine failed to process the query."
            ) from exc

        return self._to_response(request.query, result, request_id)

    @staticmethod
    def _to_response(
        query: str,
        result: EngineResult,
        request_id: str,
    ) -> QueryResponse:
        """Map an engine result onto the public response schema."""

        diagnosis = (
            Diagnosis(
                problem=result.diagnosis.problem,
                confidence=result.diagnosis.confidence,
            )
            if result.diagnosis is not None
            else None
        )

        sources = [
            Source(id=source.id, title=source.title, score=source.score)
            for source in result.sources
        ]

        return QueryResponse(
            query=query,
            language=result.language,
            answer=result.answer,
            diagnosis=diagnosis,
            sources=sources,
            request_id=request_id,
        )
