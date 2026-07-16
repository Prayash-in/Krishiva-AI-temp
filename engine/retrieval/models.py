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

    # BM25 sparse vector (parallel lists). Empty when sparse encoding was not
    # run; the vector store then indexes the document dense-only.
    sparse_indices: list[int] = Field(default_factory=list)

    sparse_values: list[float] = Field(default_factory=list)


class RetrievedChunk(DomainModel):
    """
    A knowledge chunk returned from a vector search.

    Produced by the Retriever from a vector-store hit. Carries the score so
    downstream stages (diagnosis, context assembly, citations) can rank and
    threshold results.
    """

    id: str

    title: str

    text: str

    score: float

    metadata: RetrievalMetadata