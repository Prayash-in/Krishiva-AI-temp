"""
The engine boundary contract.

The backend talks to the AI pipeline through a single facade:
``QueryEngine.answer(EngineRequest) -> EngineResult``. Everything AI —
language detection, the rule engine, retrieval, context assembly and LLM
generation — lives behind this facade, inside the engine.

These DTOs are the *internal* boundary between the backend and the engine.
They are intentionally separate from the public HTTP schemas
(:mod:`backend.schemas.query`) so the wire format and the engine's shape can
evolve independently.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from engine.knowledge_base.enums import Language


class EngineRequest(BaseModel):
    """A validated farmer query handed to the engine."""

    model_config = ConfigDict(frozen=True)

    query: str
    language: Language | None = None
    region: str | None = None
    crop: str | None = None


class EngineDiagnosis(BaseModel):
    """The engine's assessment of the underlying problem."""

    model_config = ConfigDict(frozen=True)

    problem: str
    confidence: float = Field(ge=0.0, le=1.0)


class EngineSource(BaseModel):
    """A knowledge chunk that supported the answer (for citations)."""

    model_config = ConfigDict(frozen=True)

    id: str
    title: str
    score: float | None = None
    chunk_type: str | None = None


class EngineResult(BaseModel):
    """The engine's structured response to a query."""

    model_config = ConfigDict(frozen=True)

    answer: str
    language: Language
    diagnosis: EngineDiagnosis | None = None
    sources: list[EngineSource] = Field(default_factory=list)


@runtime_checkable
class QueryEngine(Protocol):
    """The single entry point the backend uses to answer a farmer query.

    Any object exposing a compatible ``answer`` method satisfies this
    protocol (structural typing), so the real engine needs no import of the
    backend to be pluggable.
    """

    def answer(self, request: EngineRequest) -> EngineResult:
        """Answer a farmer query and return a structured result."""
        ...
