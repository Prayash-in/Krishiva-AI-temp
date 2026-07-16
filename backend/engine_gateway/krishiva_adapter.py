"""
The real :class:`QueryEngine`.

Adapts the pure knowledge engine (:mod:`engine.pipeline`) to the backend's
engine-gateway contract. The engine knows nothing about the backend; this thin
adapter maps the backend's :class:`EngineRequest` onto the engine call and the
engine's :class:`EngineAnswer` back onto the contract's :class:`EngineResult`.

Swap :class:`StubQueryEngine` for this in ``backend.main``'s lifespan.
"""

from __future__ import annotations

from engine.config import EngineConfig
from engine.generation.models import EngineAnswer
from engine.pipeline import KrishivaEngine, build_engine

from backend.engine_gateway.contract import (
    EngineDiagnosis,
    EngineRequest,
    EngineResult,
    EngineSource,
)


class KrishivaQueryEngine:
    """Backend-facing engine that delegates to the knowledge pipeline."""

    def __init__(self, engine: KrishivaEngine) -> None:
        self._engine = engine

    @classmethod
    def build(cls, config: EngineConfig | None = None) -> "KrishivaQueryEngine":
        """Construct the underlying pipeline and wrap it."""

        return cls(build_engine(config))

    def answer(self, request: EngineRequest) -> EngineResult:
        """Answer a query and map the engine result onto the contract."""

        result: EngineAnswer = self._engine.answer(
            query=request.query,
            language=request.language,
            region=request.region,
            crop=request.crop,
        )

        return EngineResult(
            answer=result.answer,
            language=result.language,
            diagnosis=(
                EngineDiagnosis(
                    problem=result.diagnosis.problem,
                    confidence=result.diagnosis.confidence,
                )
                if result.diagnosis is not None
                else None
            ),
            sources=[
                EngineSource(
                    id=source.id,
                    title=source.title,
                    score=source.score,
                    chunk_type=source.chunk_type,
                )
                for source in result.sources
            ],
        )
