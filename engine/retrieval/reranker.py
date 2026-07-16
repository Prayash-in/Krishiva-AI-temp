"""
Cross-encoder reranker.

Rescores retrieval candidates against the query with a cross-encoder
(query and passage attended jointly), which is far more accurate than the
bi-encoder similarity used for candidate generation — and its sigmoid output
is a much better-calibrated relevance signal for the diagnosis confidence.

The model is loaded lazily so importing this module stays cheap.
"""

from __future__ import annotations

import math

from sentence_transformers import CrossEncoder

from engine.retrieval.models import RetrievedChunk


class Reranker:
    """Reranks retrieved chunks with a cross-encoder relevance model."""

    def __init__(self, model_name: str = "BAAI/bge-reranker-base") -> None:
        self._model_name = model_name
        self._model: CrossEncoder | None = None

    @property
    def model(self) -> CrossEncoder:
        """Load the model on first access."""

        if self._model is None:
            self._model = CrossEncoder(self._model_name)
        return self._model

    @property
    def model_name(self) -> str:
        return self._model_name

    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        """
        Rescore chunks against the query and return them ordered by
        descending relevance, with ``score`` replaced by the reranker's
        0..1 relevance probability.
        """

        if not chunks:
            return []

        pairs = [(query, chunk.text) for chunk in chunks]
        scores = self.model.predict(pairs, convert_to_numpy=True)

        rescored = [
            chunk.model_copy(update={"score": _to_probability(float(score))})
            for chunk, score in zip(chunks, scores, strict=True)
        ]

        rescored.sort(key=lambda chunk: chunk.score, reverse=True)
        return rescored


def _to_probability(score: float) -> float:
    """
    Normalise a reranker output to 0..1.

    sentence-transformers applies a sigmoid to single-label cross-encoders by
    default; if a raw logit leaks through (custom activation / older
    versions), squash it ourselves.
    """

    if 0.0 <= score <= 1.0:
        return score
    return 1.0 / (1.0 + math.exp(-score))
