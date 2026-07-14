"""
Knowledge Base Parser.

Converts the raw authoring JSON into canonical domain models.

Responsibilities:
- Parse knowledge base metadata
- Parse knowledge chunks
- Separate metadata from structured content
- Normalize schema inconsistencies (e.g. string vs list)

Non-responsibilities:
- File loading
- Validation
- Embedding generation
- Retrieval
"""

from __future__ import annotations

from typing import Any

from .constants import (
    CATEGORY_KEY,
    CHUNK_ID_KEY,
    CHUNKS_KEY,
    CHUNK_TYPE_KEY,
    CROP_KEY,
    DATA_VERSION_KEY,
    GROWTH_STAGES_KEY,
    KB_META_KEY,
    LINKED_CHUNKS_KEY,
    LINKED_PROBLEMS_KEY,
    PRIORITY_KEY,
    PROBLEM_ID_KEY,
    PROBLEM_KEY,
    REGION_KEY,
    RETRIEVAL_TRIGGER_KEY,
    SCHEMA_VERSION_KEY,
    SEASON_KEY,
    SOURCE_KEY,
)
from .enums import ChunkType, KnowledgeCategory, Priority
from .models import (
    ChunkMetadata,
    ChunkRelationships,
    KnowledgeBase,
    KnowledgeBaseMetadata,
    KnowledgeChunk,
    StructuredContent,
)


class KnowledgeParser:
    """Parses raw dictionaries into canonical knowledge models."""

    def parse(self, raw: dict[str, Any]) -> KnowledgeBase:
        """
        Parse an entire knowledge base.

        Args:
            raw:
                Raw dictionary loaded from JSON.

        Returns:
            Parsed KnowledgeBase object.
        """

        metadata = self._parse_metadata(raw[KB_META_KEY])

        chunks = self._parse_chunks(raw[CHUNKS_KEY])

        return KnowledgeBase(
            metadata=metadata,
            chunks=chunks,
        )

    # ------------------------------------------------------------------ #
    # Metadata
    # ------------------------------------------------------------------ #

    def _parse_metadata(
        self,
        raw: dict[str, Any],
    ) -> KnowledgeBaseMetadata:
        """Parse KB metadata."""

        return KnowledgeBaseMetadata(
            crop=raw[CROP_KEY],
            problem=raw[PROBLEM_KEY],
            problem_id=raw[PROBLEM_ID_KEY],
            category=KnowledgeCategory(raw[CATEGORY_KEY]),
            region=raw[REGION_KEY],
            season=raw.get(SEASON_KEY, []),
            data_version=raw[DATA_VERSION_KEY],
            schema_version=raw[SCHEMA_VERSION_KEY],
            sources=raw.get(SOURCE_KEY, []),
            linked_problems=raw.get(LINKED_PROBLEMS_KEY, []),
        )

    # ------------------------------------------------------------------ #
    # Chunks
    # ------------------------------------------------------------------ #

    def _parse_chunks(
        self,
        raw_chunks: dict[str, dict[str, Any]],
    ) -> list[KnowledgeChunk]:
        """Parse every chunk."""

        chunks: list[KnowledgeChunk] = []

        for raw_chunk in raw_chunks.values():
            chunks.append(self._parse_chunk(raw_chunk))

        return chunks

    def _parse_chunk(
        self,
        raw: dict[str, Any],
    ) -> KnowledgeChunk:
        """Parse a single chunk."""

        # -----------------------------
        # Normalize retrieval triggers
        # -----------------------------

        triggers = raw.get(RETRIEVAL_TRIGGER_KEY, [])

        if isinstance(triggers, str):
            triggers = [triggers]

        elif triggers is None:
            triggers = []

        # -----------------------------
        # Metadata
        # -----------------------------

        metadata = ChunkMetadata(
            chunk_type=ChunkType(raw[CHUNK_TYPE_KEY]),
            priority=Priority(raw[PRIORITY_KEY]),
            growth_stages=raw.get(GROWTH_STAGES_KEY, []),
            retrieval_triggers=triggers,
        )

        # -----------------------------
        # Relationships
        # -----------------------------

        relationships = ChunkRelationships(
            related=raw.get(LINKED_CHUNKS_KEY, []),
        )

        # -----------------------------
        # Structured Content
        # -----------------------------

        content = {
            key: value
            for key, value in raw.items()
            if key
            not in {
                CHUNK_ID_KEY,
                CHUNK_TYPE_KEY,
                PRIORITY_KEY,
                GROWTH_STAGES_KEY,
                RETRIEVAL_TRIGGER_KEY,
                LINKED_CHUNKS_KEY,
            }
        }

        return KnowledgeChunk(
            id=raw[CHUNK_ID_KEY],
            metadata=metadata,
            relationships=relationships,
            content=StructuredContent(
                data=content
            ),
        )