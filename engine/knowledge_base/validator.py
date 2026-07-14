"""
Knowledge Base Validator.

Validates a parsed KnowledgeBase before indexing.

Responsibilities
----------------
- Validate duplicate chunk IDs
- Validate relationships
- Validate empty content
- Validate retrieval triggers
- Produce a validation report

The validator NEVER mutates the KnowledgeBase.
"""

from __future__ import annotations

from collections import Counter

from .enums import ChunkType
from .models import KnowledgeBase, ValidationReport
from .validation_rules import CHUNK_TYPES_REQUIRING_RETRIEVAL_TRIGGERS


class KnowledgeValidator:
    """Validates a parsed KnowledgeBase."""

    def validate(self, kb: KnowledgeBase) -> ValidationReport:
        """
        Validate a KnowledgeBase.

        Args:
            kb:
                Parsed knowledge base.

        Returns:
            ValidationReport
        """

        errors: list[str] = []
        warnings: list[str] = []

        self._validate_duplicate_chunk_ids(kb, errors)
        self._validate_relationships(kb, errors)
        self._validate_empty_content(kb, warnings)
        self._validate_retrieval_triggers(kb, warnings)

        return ValidationReport(
            valid=not errors,
            errors=errors,
            warnings=warnings,
        )

    # ------------------------------------------------------------------
    # Duplicate IDs
    # ------------------------------------------------------------------

    def _validate_duplicate_chunk_ids(
        self,
        kb: KnowledgeBase,
        errors: list[str],
    ) -> None:
        """Validate that chunk IDs are unique."""

        counts = Counter(chunk.id for chunk in kb.chunks)

        for chunk_id, count in counts.items():
            if count > 1:
                errors.append(
                    f"Duplicate chunk ID: '{chunk_id}'"
                )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def _validate_relationships(
        self,
        kb: KnowledgeBase,
        errors: list[str],
    ) -> None:
        """Validate linked chunk relationships."""

        valid_ids = {chunk.id for chunk in kb.chunks}

        for chunk in kb.chunks:

            for related_chunk in chunk.relationships.related:

                if related_chunk not in valid_ids:

                    errors.append(
                        f"Chunk '{chunk.id}' references "
                        f"unknown chunk '{related_chunk}'."
                    )

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    def _validate_empty_content(
        self,
        kb: KnowledgeBase,
        warnings: list[str],
    ) -> None:
        """Warn if a chunk contains no knowledge."""

        for chunk in kb.chunks:

            if not chunk.content.data:

                warnings.append(
                    f"Chunk '{chunk.id}' has empty content."
                )

    # ------------------------------------------------------------------
    # Retrieval Triggers
    # ------------------------------------------------------------------

    def _validate_retrieval_triggers(
        self,
        kb: KnowledgeBase,
        warnings: list[str],
    ) -> None:
        """Validate retrieval trigger quality."""

        for chunk in kb.chunks:

            if (
                chunk.metadata.chunk_type
                not in CHUNK_TYPES_REQUIRING_RETRIEVAL_TRIGGERS
            ):
                continue

            triggers = chunk.metadata.retrieval_triggers

            if not triggers:

                warnings.append(
                    f"Chunk '{chunk.id}' has no retrieval triggers."
                )

                continue

            duplicates = [
                trigger
                for trigger, count in Counter(triggers).items()
                if count > 1
            ]

            if duplicates:

                warnings.append(
                    f"Chunk '{chunk.id}' contains duplicate "
                    f"retrieval triggers: {duplicates}"
                )