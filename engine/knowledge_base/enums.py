from enum import StrEnum


class KnowledgeCategory(StrEnum):
    """Top-level knowledge category."""

    DISEASE = "disease"
    PEST = "pest"
    NUTRIENT_DEFICIENCY = "nutrient_deficiency"
    WEATHER = "weather"
    CULTURAL_PRACTICE = "cultural_practice"
    GENERAL = "general"


class ChunkType(StrEnum):
    """Type of retrievable chunk."""

    FARMER_ENTRY = "farmer_entry"

    SCIENTIFIC_SYMPTOM = "scientific_symptom"

    MANAGEMENT = "management"

    DISAMBIGUATION = "disambiguation"

    REGIONAL_CONTEXT = "regional_context"

    SYNONYM_EXPANSION = "synonym_expansion"


class Priority(StrEnum):
    """Retrieval importance."""

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


class Language(StrEnum):
    """Supported languages."""

    ENGLISH = "en"

    ASSAMESE = "as"

    HINDI = "hi"

    BENGALI = "bn"