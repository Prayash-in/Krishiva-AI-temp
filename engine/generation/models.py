"""
Engine-side answer models.

These are the engine's *own* public output shape. They are deliberately
decoupled from the backend HTTP schemas and the backend engine-gateway
contract: the backend adapts these into its contract DTOs, so the engine never
imports the backend and stays independently testable.
"""

from __future__ import annotations

from engine.knowledge_base.enums import Language
from engine.knowledge_base.models import DomainModel
from pydantic import Field


class AnswerDiagnosis(DomainModel):
    """The engine's assessment of the underlying problem."""

    problem: str

    problem_id: str

    confidence: float = Field(ge=0.0, le=1.0)


class AnswerSource(DomainModel):
    """A knowledge chunk that supported the answer (for citations)."""

    id: str

    title: str

    score: float

    chunk_type: str

    problem_id: str


class EngineAnswer(DomainModel):
    """The engine's structured response to a farmer query."""

    answer: str

    language: Language

    diagnosis: AnswerDiagnosis | None = None

    sources: list[AnswerSource] = Field(default_factory=list)
