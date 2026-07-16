"""
Embedding service for retrieval documents.

Responsibilities:
- Load the embedding model (lazily)
- Generate document embeddings (for indexing)
- Generate query embeddings (for retrieval)
- Return IndexedDocuments

The model is loaded lazily on first use so importing this module (e.g. from
the backend during startup) does not force a multi-hundred-MB model download
before it is actually needed.
"""

from __future__ import annotations

from sentence_transformers import SentenceTransformer

from engine.retrieval.models import (
    IndexedDocument,
    RetrievalDocument,
)

# bge-* retrieval models expect a short instruction prefixed to the *query*
# (not the documents) to align the query and passage embedding spaces.
_BGE_QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "


class Embedder:
    """Converts RetrievalDocuments into IndexedDocuments and embeds queries."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ) -> None:

        self._model_name = model_name
        self._model: SentenceTransformer | None = None

    # ------------------------------------------------------------------
    # Model access (lazy)
    # ------------------------------------------------------------------

    @property
    def model(self) -> SentenceTransformer:
        """Load the model on first access."""

        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
        return self._model

    # ------------------------------------------------------------------
    # Documents
    # ------------------------------------------------------------------

    def embed(
        self,
        documents: list[RetrievalDocument],
        batch_size: int = 32,
        show_progress_bar: bool = False,
    ) -> list[IndexedDocument]:
        """
        Generate embeddings for retrieval documents.

        Parameters
        ----------
        documents
            Retrieval documents.
        batch_size
            Encoding batch size.
        show_progress_bar
            Whether to show a tqdm progress bar.

        Returns
        -------
        list[IndexedDocument]
        """

        if not documents:
            return []

        texts = [document.text for document in documents]

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        indexed_documents: list[IndexedDocument] = []

        for document, embedding in zip(documents, embeddings, strict=True):
            indexed_documents.append(
                IndexedDocument(
                    id=document.id,
                    title=document.title,
                    text=document.text,
                    metadata=document.metadata,
                    embedding=embedding.tolist(),
                )
            )

        return indexed_documents

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def embed_query(self, query: str) -> list[float]:
        """Embed a search query (with the bge query instruction)."""

        text = f"{_BGE_QUERY_INSTRUCTION}{query}"

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    @property
    def embedding_dimension(self) -> int:
        # Prefer the newer method name; fall back for older sentence-transformers.
        getter = getattr(self.model, "get_embedding_dimension", None)
        if getter is None:
            getter = self.model.get_sentence_embedding_dimension
        return getter()

    @property
    def model_name(self) -> str:
        return self._model_name
