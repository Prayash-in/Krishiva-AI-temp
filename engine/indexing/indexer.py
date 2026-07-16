"""
Knowledge-base indexer.

The offline write-path that turns authored knowledge JSON into a searchable
vector store:

    every KB json under kb_dir
        -> Loader -> Parser -> (Validator) -> Formatter
        -> Embedder -> VectorStore

This is intentionally a batch/offline operation. The embedded Qdrant store
holds a file lock, so the index must be built while the backend is NOT holding
the same store open.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from engine.config import EngineConfig
from engine.knowledge_base.loader import KnowledgeLoader
from engine.knowledge_base.parser import KnowledgeParser
from engine.knowledge_base.validator import KnowledgeValidator
from engine.retrieval.embedder import Embedder
from engine.retrieval.formatting.formatter import TemplateFormatter
from engine.retrieval.models import RetrievalDocument
from engine.retrieval.sparse import BM25SparseEncoder
from engine.retrieval.vector_store import VectorStore


@dataclass(frozen=True)
class IndexSummary:
    """Result of an index build."""

    kb_count: int
    chunk_count: int
    vector_count: int
    dimension: int
    problems: list[str]


class Indexer:
    """Builds the vector store from all knowledge bases under a directory."""

    def __init__(
        self,
        config: EngineConfig | None = None,
        embedder: Embedder | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self._config = config or EngineConfig.from_env()
        self._embedder = embedder or Embedder(self._config.embedding_model)
        self._store = vector_store or VectorStore(
            collection_name=self._config.collection_name,
            path=str(self._config.vector_store_path),
        )
        self._loader = KnowledgeLoader()
        self._parser = KnowledgeParser()
        self._validator = KnowledgeValidator()
        self._formatter = TemplateFormatter()

    # ------------------------------------------------------------------

    def discover(self) -> list[Path]:
        """Return all knowledge JSON files under the KB directory (sorted)."""

        return sorted(self._config.kb_dir.rglob("*.json"))

    def build(
        self,
        rebuild: bool = True,
        show_progress_bar: bool = True,
    ) -> IndexSummary:
        """
        Build (or rebuild) the vector index over every knowledge base.

        Parameters
        ----------
        rebuild
            When True (default) the collection is dropped and recreated so the
            index exactly mirrors the current knowledge on disk.
        """

        kb_files = self.discover()
        if not kb_files:
            raise FileNotFoundError(
                f"No knowledge JSON files found under {self._config.kb_dir}"
            )

        documents: list[RetrievalDocument] = []
        problems: list[str] = []
        kb_count = 0

        for kb_file in kb_files:
            raw = self._loader.load_json(kb_file)
            kb = self._parser.parse(raw)

            report = self._validator.validate(kb)
            if not report.valid:
                logger.warning(
                    "KB {} has validation errors: {}",
                    kb_file.name,
                    report.errors,
                )
            for warning in report.warnings:
                logger.debug("KB {} warning: {}", kb_file.name, warning)

            kb_count += 1
            problems.append(kb.metadata.problem)

            for chunk in kb.chunks:
                documents.append(self._formatter.format(chunk, kb.metadata))

            logger.info(
                "Formatted {} chunks from {} ({})",
                len(kb.chunks),
                kb.metadata.problem,
                kb_file.name,
            )

        logger.info("Embedding {} documents...", len(documents))
        indexed = self._embedder.embed(
            documents, show_progress_bar=show_progress_bar
        )
        dimension = self._embedder.embedding_dimension

        logger.info("BM25-encoding {} documents...", len(indexed))
        sparse_encodings = BM25SparseEncoder().encode_documents(
            [document.text for document in indexed]
        )
        indexed = [
            document.model_copy(
                update={
                    "sparse_indices": encoding.indices,
                    "sparse_values": encoding.values,
                }
            )
            for document, encoding in zip(indexed, sparse_encodings, strict=True)
        ]

        if rebuild:
            self._store.delete_collection()
        self._store.create_collection(vector_size=dimension)
        self._store.upsert(indexed)

        vector_count = self._store.count()

        logger.info(
            "Index built: {} KBs, {} chunks, {} vectors (dim={})",
            kb_count,
            len(documents),
            vector_count,
            dimension,
        )

        return IndexSummary(
            kb_count=kb_count,
            chunk_count=len(documents),
            vector_count=vector_count,
            dimension=dimension,
            problems=problems,
        )
