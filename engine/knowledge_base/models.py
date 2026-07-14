"""
Canonical domain models for the Krishiva Knowledge Engine.

These models represent agricultural knowledge independently of:
- JSON storage
- Vector databases
- LLM providers
- FastAPI
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import ChunkType, KnowledgeCategory, Priority


class DomainModel(BaseModel):
    """Base model for all immutable domain objects."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class KnowledgeBaseMetadata(DomainModel):
    """Metadata describing an entire knowledge base."""

    crop: str

    problem: str

    problem_id: str

    category: KnowledgeCategory

    region: str

    season: list[str] = Field(default_factory=list)

    data_version: str

    schema_version: str

    sources: list[str] = Field(default_factory=list)

    linked_problems: list[str] = Field(default_factory=list)


class ChunkMetadata(DomainModel):
    """Metadata used during retrieval and filtering."""

    chunk_type: ChunkType

    priority: Priority

    growth_stages: list[str] = Field(default_factory=list)

    retrieval_triggers: list[str] = Field(default_factory=list)

    # tags: list[str] = Field(default_factory=list)

    # languages: list[str] = Field(default_factory=list)

    region: str | None = None

    # source: str | None = None


class StructuredContent(DomainModel):
    """
    Structured agricultural knowledge.

    Raw knowledge is preserved here exactly as parsed.
    Formatter classes later convert this into retrieval text.
    """

    data: dict[str, Any] = Field(default_factory=dict)


class ChunkRelationships(DomainModel):
    """Relationships between knowledge chunks."""

    related: list[str] = Field(default_factory=list)

    parent: str | None = None

    children: list[str] = Field(default_factory=list)


class KnowledgeChunk(DomainModel):
    """Canonical unit of agricultural knowledge."""

    id: str

    metadata: ChunkMetadata

    content: StructuredContent

    relationships: ChunkRelationships = Field(
        default_factory=ChunkRelationships
    )


class KnowledgeBase(DomainModel):
    """Canonical agricultural knowledge base."""

    metadata: KnowledgeBaseMetadata

    chunks: list[KnowledgeChunk] = Field(default_factory=list)

class ValidationReport(DomainModel):
    """Validation result for a KnowledgeBase."""

    valid: bool

    errors: list[str] = Field(default_factory=list)

    warnings: list[str] = Field(default_factory=list)