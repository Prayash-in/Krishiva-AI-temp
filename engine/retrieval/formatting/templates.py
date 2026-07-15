"""
Formatting templates for RetrievalDocuments.

Each template defines the order and rendering type
for fields in a KnowledgeChunk.
"""

from __future__ import annotations

from engine.knowledge_base.enums import ChunkType
from engine.retrieval.enums import RenderType

# tuple format:
# (Section Title, Content Key, Renderer Type)

TEMPLATES = {

    ChunkType.FARMER_ENTRY: [

        ("Common Farmer Descriptions",
         "farmer_phrases",
         RenderType.MULTILINGUAL_LIST),

        ("What Farmer Sees First",
         "what_farmer_sees_first",
         "text"),

        ("Visual Description",
         "visual_description_farmer",
         "text"),

        ("How to Confirm",
         "farmer_confirmation_step",
         "text"),

        ("Typical Blast Symptoms",
         "this_is_blast_if",
         RenderType.LIST),

        ("Not Blast If",
         "not_blast_if",
         "list"),

        ("Urgency",
         "urgency",
         RenderType.TEXT),

        ("Economic Threshold",
         "economic_threshold",
         "text"),
    ],

    ChunkType.SCIENTIFIC_SYMPTOM: [

    (
        "Blast Types",
        "blast_types",
        RenderType.LIST_OF_OBJECTS,
    ),

    (
        "Diagnostic Markers",
        "diagnostic_markers",
        RenderType.LIST,
    ),

    (
        "Pathogen Biology",
        "pathogen_biology",
        RenderType.KEY_VALUE,
    ),

    (
        "Favorable Conditions",
        "favorable_conditions",
        RenderType.KEY_VALUE,
    ),

    (
        "Symptom Tags",
        "symptom_tags",
        RenderType.LIST,
    ),

    (
        "Crop Parts Affected",
        "crop_parts_affected",
        RenderType.LIST,
    ),
    ],

    ChunkType.DISAMBIGUATION: [

    (
        "Always Retrieve With",
        "always_retrieve_with",
        RenderType.LIST,
    ),

    (
        "Disambiguation Tree",
        "disambiguation_trees",
        RenderType.KEY_VALUE_GROUP,
    ),

    (
        "One Sentence Differentiators",
        "one_sentence_differentiators",
        RenderType.KEY_VALUE_GROUP,
    ),

    (
        "False Positive Risk Ratings",
        "false_positive_risk_ratings",
        RenderType.KEY_VALUE_GROUP,
    ),
    ],

    ChunkType.MANAGEMENT: [

        ("Cultural Management",
         "cultural_management",
         "list"),

        ("Biological Management",
         "biological_management",
         "list"),

        ("Chemical Management",
         "chemical_management",
         RenderType.KEY_VALUE_GROUP),
    ],

    ChunkType.REGIONAL_CONTEXT: [

    (
        "Seasonal Risk Calendar",
        "seasonal_risk_calendar",
        RenderType.KEY_VALUE_GROUP,
    ),

    (
        "Susceptible Varieties",
        "assam_susceptible_varieties",
        RenderType.KEY_VALUE,
    ),

    (
        "Resistant Varieties",
        "assam_resistant_varieties",
        RenderType.KEY_VALUE,
    ),

    (
        "Flood Interaction",
        "flood_blast_interaction",
        RenderType.KEY_VALUE,
    ),

    (
        "Local Pesticide Availability",
        "local_pesticide_availability",
        RenderType.KEY_VALUE,
    ),

    (
        "Extension Contact",
        "extension_contact",
        RenderType.KEY_VALUE,
    ),
    ],

    ChunkType.SYNONYM_EXPANSION: [

    (
        "Canonical Disease Terms",
        "canonical_disease_terms",
        RenderType.LIST,
    ),

    (
        "Farmer Synonyms",
        "farmer_synonyms_by_language",
        RenderType.MULTILINGUAL_LIST,
    ),

    (
        "Shape Synonyms",
        "shape_synonyms",
        RenderType.KEY_VALUE,
    ),

    (
        "Color Synonyms",
        "color_synonyms",
        RenderType.KEY_VALUE,
    ),

    (
        "Location Synonyms",
        "location_synonyms",
        RenderType.KEY_VALUE,
    ),

    (
        "Action Synonyms",
        "action_synonyms",
        RenderType.KEY_VALUE,
    ),

    (
        "Environmental Boosters",
        "environmental_co_occurrence_boosters",
        RenderType.LIST,
    ),

    (
        "Negative Keywords",
        "negative_keywords",
        RenderType.KEY_VALUE,
    ),

    (
        "Confirmed False Positives",
        "confirmed_false_positives",
        RenderType.LIST,
    ),
    ],
}