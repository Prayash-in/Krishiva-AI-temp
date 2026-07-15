"""
Canonical retrieval models.

These models are independent of:
- Knowledge authoring schema
- Embedding model
- Vector database
"""

from __future__ import annotations

from pydantic import Field

from engine.knowledge_base.models import DomainModel

from engine.knowledge_base.enums import (
    ChunkType,
    Priority,
)

class RetrievalMetadata(DomainModel):
    """
    Metadata attached to every retrieval document.

    Used for:
    - filtering
    - debugging
    - reranking
    - citations
    """

    crop: str

    problem: str

    problem_id: str

    region: str

    chunk_type: ChunkType

    priority: Priority

    growth_stages: list[str] = Field(default_factory=list)


class RetrievalDocument(DomainModel):
    """
    Canonical retrieval document.

    Produced by the formatter.
    Consumed by the embedder.
    """

    id: str

    title: str

    text: str

    metadata: RetrievalMetadata


class IndexedDocument(DomainModel):
    """
    Retrieval document with embedding.

    Stored inside the vector database.
    """

    id: str

    title: str

    text: str

    metadata: RetrievalMetadata

    embedding: list[float]