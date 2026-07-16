"""
Retriever.

Ties the Embedder, the VectorStore and the Reranker together into the read
path of the retrieval layer:

    query text
        -> Embedder.embed_query + BM25 query encoding
        -> VectorStore.hybrid_search (dense + BM25, RRF fusion)
        -> Reranker (cross-encoder rescoring)
        -> problem-diversity cap
        -> RetrievedChunk domain models

It is deliberately thin: no LLM, no formatting, no knowledge-base awareness.
"""

from __future__ import annotations

from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
    ScoredPoint,
)

from engine.knowledge_base.enums import ChunkType, Priority
from engine.retrieval.embedder import Embedder
from engine.retrieval.models import RetrievedChunk, RetrievalMetadata
from engine.retrieval.reranker import Reranker
from engine.retrieval.sparse import BM25SparseEncoder, SparseEncoding
from engine.retrieval.vector_store import VectorStore

# How many hybrid candidates to pull before reranking. Wider than top_k so the
# cross-encoder gets a real shot at recovering chunks the fusion under-ranked.
_CANDIDATE_POOL = 20

# Maximum chunks per problem in the final result, so the LLM sees competing
# diagnoses when they exist instead of top_k chunks about a single problem.
_MAX_PER_PROBLEM = 3


class Retriever:
    """Hybrid (dense + BM25) search with cross-encoder reranking."""

    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
        reranker: Reranker | None = None,
        sparse_encoder: BM25SparseEncoder | None = None,
    ) -> None:
        self._embedder = embedder
        self._store = vector_store
        self._reranker = reranker
        self._sparse_encoder = sparse_encoder or BM25SparseEncoder()

    def retrieve(
        self,
        query: str,
        top_k: int = 6,
        crop: str | None = None,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant knowledge chunks for a query.

        Parameters
        ----------
        query
            The farmer's question (raw text).
        top_k
            Maximum number of chunks to return.
        crop
            Optional crop hint. When it matches an indexed crop the search is
            restricted to that crop; a non-matching hint is ignored rather than
            returning nothing.

        Returns
        -------
        list[RetrievedChunk]
            Ordered by descending relevance. When a reranker is configured,
            ``score`` is its 0..1 relevance probability; otherwise it is the
            fusion score.
        """

        if not query or not query.strip():
            return []

        query_embedding = self._embedder.embed_query(query)
        sparse = self._sparse_encoder.encode_query(query)
        pool = max(_CANDIDATE_POOL, top_k)

        query_filter = self._build_filter(crop)

        points = self._search(query_embedding, sparse, pool, query_filter)

        # A crop filter can legitimately produce zero hits (e.g. the hint names
        # a crop we do not have knowledge for yet). Fall back to an unfiltered
        # search so the farmer still gets the best-available answer.
        if not points and query_filter is not None:
            points = self._search(query_embedding, sparse, pool, None)

        chunks = [self._to_chunk(point) for point in points]

        if self._reranker is not None:
            chunks = self._reranker.rerank(query, chunks)

        return self._diversify(chunks, top_k)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _search(
        self,
        query_embedding: list[float],
        sparse: SparseEncoding,
        pool: int,
        query_filter: Filter | None,
    ) -> list[ScoredPoint]:
        return self._store.hybrid_search(
            query_embedding=query_embedding,
            sparse_indices=sparse.indices,
            sparse_values=sparse.values,
            top_k=pool,
            query_filter=query_filter,
        )

    @staticmethod
    def _diversify(
        chunks: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """
        Take the top_k chunks while capping how many any single problem may
        contribute. Capped-out chunks backfill the result if the diverse set
        alone cannot reach top_k.
        """

        selected: list[RetrievedChunk] = []
        overflow: list[RetrievedChunk] = []
        per_problem: dict[str, int] = {}

        for chunk in chunks:
            key = chunk.metadata.problem_id or chunk.metadata.problem
            if per_problem.get(key, 0) < _MAX_PER_PROBLEM:
                selected.append(chunk)
                per_problem[key] = per_problem.get(key, 0) + 1
            else:
                overflow.append(chunk)
            if len(selected) == top_k:
                return selected

        selected.extend(overflow[: top_k - len(selected)])
        return selected

    @staticmethod
    def _build_filter(crop: str | None) -> Filter | None:
        """Build a case-insensitive crop filter, if a crop was provided."""

        if not crop or not crop.strip():
            return None

        # Payload crops are stored title-cased (e.g. "Rice"); normalise the
        # hint so "rice" / "RICE" still match.
        normalised = crop.strip().title()

        return Filter(
            must=[
                FieldCondition(
                    key="crop",
                    match=MatchValue(value=normalised),
                )
            ]
        )

    @staticmethod
    def _to_chunk(point: ScoredPoint) -> RetrievedChunk:
        """Reconstruct a RetrievedChunk from a vector-store hit."""

        payload = point.payload or {}

        metadata = RetrievalMetadata(
            crop=payload.get("crop", ""),
            problem=payload.get("problem", ""),
            problem_id=payload.get("problem_id", ""),
            region=payload.get("region", ""),
            chunk_type=ChunkType(payload["chunk_type"]),
            priority=Priority(payload["priority"]),
            growth_stages=payload.get("growth_stages", []) or [],
        )

        return RetrievedChunk(
            id=payload.get("document_id", str(point.id)),
            title=payload.get("title", ""),
            text=payload.get("text", ""),
            score=float(point.score),
            metadata=metadata,
        )
