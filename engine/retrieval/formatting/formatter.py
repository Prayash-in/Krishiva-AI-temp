"""
Generic template-driven formatter.

Converts a KnowledgeChunk into a RetrievalDocument.
"""

from __future__ import annotations

from engine.knowledge_base.models import (
    KnowledgeBaseMetadata,
    KnowledgeChunk,
)
from engine.retrieval.enums import RenderType
from engine.retrieval.models import (
    RetrievalDocument,
    RetrievalMetadata,
)

from .builder import TextBuilder
from .templates import TEMPLATES


class TemplateFormatter:
    """Formats KnowledgeChunks into RetrievalDocuments."""

    def format(
        self,
        chunk: KnowledgeChunk,
        kb_metadata: KnowledgeBaseMetadata,
    ) -> RetrievalDocument:

        builder = TextBuilder()

        # --------------------------------------------------
        # Global Context
        # --------------------------------------------------

        builder.field("Crop", kb_metadata.crop)
        builder.field("Problem", kb_metadata.problem)
        builder.field("Region", kb_metadata.region)

        builder.text("")

        content = chunk.content.data

        template = TEMPLATES[chunk.metadata.chunk_type]

        # --------------------------------------------------
        # Build Document
        # --------------------------------------------------

        for section_title, field_name, render_type in template:

            value = content.get(field_name)

            if value is None:
                continue

            builder.section(section_title)

            match render_type:

                case RenderType.TEXT:

                    builder.text(str(value))

                case RenderType.LIST:

                    if isinstance(value, list):
                        builder.bullets(value)
                    else:
                        builder.text(str(value))

                case RenderType.MULTILINGUAL_LIST:

                    if isinstance(value, dict):
                        builder.multilingual_bullets(value)
                    else:
                        builder.text(str(value))

                case RenderType.KEY_VALUE:

                    if isinstance(value, dict):
                        builder.key_value(value)
                    else:
                        builder.text(str(value))

                case RenderType.KEY_VALUE_GROUP:

                    if isinstance(value, dict):
                        builder.key_value_group(value)
                    else:
                        builder.text(str(value))

                case RenderType.LIST_OF_OBJECTS:

                    if isinstance(value, list):
                        builder.list_of_objects(value)
                    else:
                        builder.text(str(value))

                case _:

                    raise ValueError(
                        f"Unsupported render type: {render_type}"
                    )

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = RetrievalMetadata(
            crop=kb_metadata.crop,
            problem=kb_metadata.problem,
            problem_id=kb_metadata.problem_id,
            region=kb_metadata.region,
            chunk_type=chunk.metadata.chunk_type,
            priority=chunk.metadata.priority,
            growth_stages=chunk.metadata.growth_stages,
        )

        # --------------------------------------------------
        # Retrieval Document
        # --------------------------------------------------

        return RetrievalDocument(
            id=chunk.id,
            title=(
                f"{kb_metadata.problem} | "
                f"{chunk.metadata.chunk_type.value.replace('_', ' ').title()}"
            ),
            text=builder.build(),
            metadata=metadata,
        )