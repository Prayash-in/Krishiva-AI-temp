"""
Knowledge Base validation rules.
"""

from .enums import ChunkType

CHUNK_TYPES_REQUIRING_RETRIEVAL_TRIGGERS = {
    ChunkType.FARMER_ENTRY,
    ChunkType.MANAGEMENT,
    ChunkType.SCIENTIFIC_SYMPTOM,
    ChunkType.DISAMBIGUATION,
    ChunkType.REGIONAL_CONTEXT,
}