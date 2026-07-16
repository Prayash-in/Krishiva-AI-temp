"""
Public HTTP schemas for the query endpoint.

These define the wire contract for ``POST /api/v1/query`` and are kept
separate from the engine DTOs so the API can evolve independently of the
engine's internal shape.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from engine.knowledge_base.enums import Language

_MAX_QUERY_LENGTH = 1000


class QueryRequest(BaseModel):
    """A farmer query submitted to the assistant."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "query": "yellow spot on my paddy leaf",
                "language": "en",
                "region": "Assam",
                "crop": "rice",
            }
        },
    )

    query: str = Field(
        min_length=1,
        max_length=_MAX_QUERY_LENGTH,
        description="The farmer's question, in any supported language.",
    )
    language: Language | None = Field(
        default=None,
        description="Optional language hint; the engine detects it otherwise.",
    )
    region: str | None = Field(default=None, max_length=100)
    crop: str | None = Field(default=None, max_length=100)

    @field_validator("query")
    @classmethod
    def _reject_blank(cls, value: str) -> str:
        """Ensure the query is not empty once surrounding whitespace is removed."""

        if not value.strip():
            raise ValueError("query must not be empty")
        return value


class Diagnosis(BaseModel):
    """The assessed problem behind a query."""

    problem: str
    confidence: float = Field(ge=0.0, le=1.0)


class Source(BaseModel):
    """A knowledge source cited in the answer."""

    id: str
    title: str
    score: float | None = None


class QueryResponse(BaseModel):
    """The structured answer returned to the client."""

    query: str
    language: Language
    answer: str
    diagnosis: Diagnosis | None = None
    sources: list[Source] = Field(default_factory=list)
    request_id: str
