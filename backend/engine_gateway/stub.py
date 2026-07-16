"""
A stub implementation of :class:`QueryEngine`.

This is a placeholder that returns a deterministic, plausible Rice Blast
result so the API is runnable end-to-end and the frontend can integrate
against the real response shape while the actual engine is being built.

It performs no retrieval, rule evaluation or LLM generation. Swap it for the
real engine in :func:`backend.main.create_app`'s lifespan when ready.
"""

from __future__ import annotations

from engine.knowledge_base.enums import Language

from backend.engine_gateway.contract import (
    EngineDiagnosis,
    EngineRequest,
    EngineResult,
    EngineSource,
)

_STUB_ANSWER = (
    "This looks like it may be Rice Blast, a fungal disease. Check whether the "
    "leaf spots are diamond or eye shaped with a gray or ash-white center and a "
    "brown border. If confirmed, avoid applying more nitrogen and consider a "
    "Tricyclazole spray at the early stage. (Placeholder response — the "
    "knowledge engine is not yet connected.)"
)

_STUB_SOURCES = (
    EngineSource(
        id="blast_farmer_entry_leaf_001",
        title="Rice Blast | Farmer Entry",
        score=0.82,
        chunk_type="farmer_entry",
    ),
    EngineSource(
        id="blast_management_tillering_001",
        title="Rice Blast | Management",
        score=0.74,
        chunk_type="management",
    ),
)


class StubQueryEngine:
    """A canned :class:`QueryEngine` used until the real engine lands."""

    def answer(self, request: EngineRequest) -> EngineResult:
        """Return a fixed Rice Blast result, echoing the requested language."""

        return EngineResult(
            answer=_STUB_ANSWER,
            language=request.language or Language.ENGLISH,
            diagnosis=EngineDiagnosis(problem="Rice Blast", confidence=0.5),
            sources=list(_STUB_SOURCES),
        )
