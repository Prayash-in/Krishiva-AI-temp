"""
Qdrant vector store implementation.

Responsibilities:
- Create/Delete collection
- Upsert indexed documents
- Count stored vectors
- Search vectors (dense-only or hybrid dense+BM25 with RRF fusion)

The collection stores two vectors per point:
- "dense": the embedding (cosine)
- "bm25":  a sparse BM25 vector; Qdrant applies IDF server-side
           (``Modifier.IDF``), so the client only supplies term-frequency
           weights.

The VectorStore is intentionally independent of:
- Knowledge Base
- Formatter
- Embedder

It only works with IndexedDocument.
"""

from __future__ import annotations

import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    Filter,
    Fusion,
    FusionQuery,
    Modifier,
    PointStruct,
    Prefetch,
    ScoredPoint,
    SparseVector,
    SparseVectorParams,
    VectorParams,
)

from engine.retrieval.models import IndexedDocument

# Stable namespace so a chunk's document id always maps to the same Qdrant
# point id. This makes upserts idempotent and, crucially, keeps point ids
# unique across knowledge bases (a per-call ``enumerate`` index would collide
# when indexing more than one KB into the same collection).
_POINT_ID_NAMESPACE = uuid.UUID("f5b2c0de-4a1e-4c2a-9f2d-6b7c8d9e0a1b")

DENSE_VECTOR_NAME = "dense"
SPARSE_VECTOR_NAME = "bm25"


def _point_id(document_id: str) -> str:
    """Return a deterministic UUID point id for a document id."""

    return str(uuid.uuid5(_POINT_ID_NAMESPACE, document_id))


class VectorStore:
    """Persistent vector storage backed by Qdrant."""

    def __init__(
        self,
        collection_name: str = "krishiva_kb",
        path: str = "data/vector_store",
    ) -> None:
        self.collection_name = collection_name
        self.client = QdrantClient(path=path)

    # ------------------------------------------------------------------
    # Collection Management
    # ------------------------------------------------------------------

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        """Create collection if it does not already exist."""

        if self.collection_exists():
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                DENSE_VECTOR_NAME: VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            },
            sparse_vectors_config={
                SPARSE_VECTOR_NAME: SparseVectorParams(
                    modifier=Modifier.IDF,
                ),
            },
        )

    def delete_collection(self) -> None:
        """Delete collection if it exists."""

        if self.collection_exists():
            self.client.delete_collection(self.collection_name)

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def upsert(
        self,
        documents: list[IndexedDocument],
    ) -> None:
        """Insert or update indexed documents."""

        if not documents:
            return

        points: list[PointStruct] = []

        for document in documents:

            payload = {
                "document_id": document.id,
                "title": document.title,
                "text": document.text,
                "crop": document.metadata.crop,
                "problem": document.metadata.problem,
                "problem_id": document.metadata.problem_id,
                "region": document.metadata.region,
                "chunk_type": document.metadata.chunk_type.value,
                "priority": document.metadata.priority.value,
                "growth_stages": document.metadata.growth_stages,
            }

            vector: dict[str, Any] = {DENSE_VECTOR_NAME: document.embedding}
            if document.sparse_indices:
                vector[SPARSE_VECTOR_NAME] = SparseVector(
                    indices=document.sparse_indices,
                    values=document.sparse_values,
                )

            points.append(
                PointStruct(
                    id=_point_id(document.id),
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        query_filter: Filter | None = None,
    ) -> list[ScoredPoint]:
        """
        Dense-only similarity search.

        Returns raw ScoredPoint objects.
        The Retriever transforms them into domain models.
        """

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            using=DENSE_VECTOR_NAME,
            query_filter=query_filter,
            limit=top_k,
        ).points

    def hybrid_search(
        self,
        query_embedding: list[float],
        sparse_indices: list[int],
        sparse_values: list[float],
        top_k: int = 5,
        query_filter: Filter | None = None,
    ) -> list[ScoredPoint]:
        """
        Hybrid dense + BM25 search fused with Reciprocal Rank Fusion.

        Falls back to dense-only when the query produced no sparse terms
        (e.g. a stopword-only query).
        """

        if not sparse_indices:
            return self.search(
                query_embedding=query_embedding,
                top_k=top_k,
                query_filter=query_filter,
            )

        prefetch = [
            Prefetch(
                query=query_embedding,
                using=DENSE_VECTOR_NAME,
                filter=query_filter,
                limit=top_k,
            ),
            Prefetch(
                query=SparseVector(
                    indices=sparse_indices,
                    values=sparse_values,
                ),
                using=SPARSE_VECTOR_NAME,
                filter=query_filter,
                limit=top_k,
            ),
        ]

        return self.client.query_points(
            collection_name=self.collection_name,
            prefetch=prefetch,
            query=FusionQuery(fusion=Fusion.RRF),
            limit=top_k,
        ).points

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def count(self) -> int:
        """Return number of vectors stored."""

        return self.client.count(
            collection_name=self.collection_name,
            exact=True,
        ).count

    def collection_exists(self) -> bool:
        """Check whether the collection exists."""

        existing = {
            collection.name
            for collection in self.client.get_collections().collections
        }

        return self.collection_name in existing

    def collection_info(self) -> dict[str, Any]:
        """Return collection information."""

        return self.client.get_collection(self.collection_name).model_dump()
