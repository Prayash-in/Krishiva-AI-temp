"""
Enums used by the retrieval layer.
"""

from enum import StrEnum


class RenderType(StrEnum):
    """Supported rendering strategies for formatter templates."""

    TEXT = "text"

    LIST = "list"

    MULTILINGUAL_LIST = "multilingual_list"
    
    KEY_VALUE = "key_value"
    
    KEY_VALUE_GROUP = "key_value_group"

    LIST_OF_OBJECTS = "list_of_objects"