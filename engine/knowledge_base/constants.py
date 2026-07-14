"""
Constants representing the Knowledge Base authoring schema.

Keeping schema keys centralized avoids magic strings and makes
schema evolution easier.
"""

# =============================================================================
# Root Keys
# =============================================================================

KB_META_KEY = "kb_meta"
CHUNKS_KEY = "chunks"
RETRIEVAL_CONFIG_KEY = "retrieval_config"

# =============================================================================
# Knowledge Base Metadata
# =============================================================================

CROP_KEY = "crop"
PROBLEM_KEY = "problem"
PROBLEM_ID_KEY = "problem_id"
CATEGORY_KEY = "category"
REGION_KEY = "region"
SEASON_KEY = "season"
DATA_VERSION_KEY = "data_version"
SCHEMA_VERSION_KEY = "schema_version"
SOURCE_KEY = "source"
LINKED_PROBLEMS_KEY = "linked_problems"

# =============================================================================
# Chunk Metadata
# =============================================================================

CHUNK_ID_KEY = "chunk_id"
CHUNK_TYPE_KEY = "chunk_type"
PRIORITY_KEY = "priority"
GROWTH_STAGES_KEY = "growth_stages"
RETRIEVAL_TRIGGER_KEY = "retrieval_trigger"
LINKED_CHUNKS_KEY = "linked_chunks"

# These keys belong to metadata and should not remain in content.
METADATA_KEYS = {
    CHUNK_ID_KEY,
    CHUNK_TYPE_KEY,
    PRIORITY_KEY,
    GROWTH_STAGES_KEY,
    RETRIEVAL_TRIGGER_KEY,
    LINKED_CHUNKS_KEY,
}