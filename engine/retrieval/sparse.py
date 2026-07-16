"""
BM25 sparse encoding for hybrid retrieval.

Produces Qdrant sparse vectors that, combined with the collection's
``Modifier.IDF``, implement BM25 scoring server-side:

- Document side: each term's value is the BM25 term-frequency saturation
  component (k1/b weighting against the corpus average length). Qdrant
  multiplies it by the IDF of the term at query time.
- Query side: each unique term has weight 1.0 (the standard BM25 query form).

Terms are mapped to stable uint32 indices by hashing, so no vocabulary needs
to be persisted between indexing and querying.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass

_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Minimal English stopword list; enough to keep function words from dominating
# the sparse match without pulling in an NLP dependency.
_STOPWORDS = frozenset(
    """
    a an and are as at be by for from has have how in is it its of on or
    that the this to was what when where which who will with you your can
    do does did should would could my i we they he she them their our
    """.split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase alphanumeric tokens with stopwords removed."""

    return [
        token
        for token in _TOKEN_RE.findall(text.lower())
        if len(token) > 1 and token not in _STOPWORDS
    ]


def _term_index(token: str) -> int:
    """Stable uint32 index for a term (first 4 bytes of its MD5)."""

    return int.from_bytes(hashlib.md5(token.encode("utf-8")).digest()[:4], "big")


@dataclass(frozen=True)
class SparseEncoding:
    """A sparse vector as parallel index/value lists."""

    indices: list[int]
    values: list[float]


class BM25SparseEncoder:
    """Encodes documents and queries as BM25 sparse vectors."""

    def __init__(self, k1: float = 1.2, b: float = 0.75) -> None:
        self._k1 = k1
        self._b = b

    def encode_documents(self, texts: list[str]) -> list[SparseEncoding]:
        """Encode a corpus (average length is computed over ``texts``)."""

        if not texts:
            return []

        token_lists = [tokenize(text) for text in texts]
        total = sum(len(tokens) for tokens in token_lists)
        avg_len = (total / len(token_lists)) or 1.0

        return [self._encode_document(tokens, avg_len) for tokens in token_lists]

    def _encode_document(
        self, tokens: list[str], avg_len: float
    ) -> SparseEncoding:
        if not tokens:
            return SparseEncoding(indices=[], values=[])

        counts = Counter(tokens)
        doc_len = len(tokens)
        norm = self._k1 * (1 - self._b + self._b * doc_len / avg_len)

        indices: list[int] = []
        values: list[float] = []
        for token, tf in counts.items():
            indices.append(_term_index(token))
            values.append(tf * (self._k1 + 1) / (tf + norm))

        return SparseEncoding(indices=indices, values=values)

    @staticmethod
    def encode_query(query: str) -> SparseEncoding:
        """Encode a query: unique terms, unit weights."""

        unique = set(tokenize(query))
        return SparseEncoding(
            indices=[_term_index(token) for token in unique],
            values=[1.0] * len(unique),
        )
