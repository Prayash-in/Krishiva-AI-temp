"""
Knowledge Base Loader.

Responsible only for reading knowledge files from disk.

Responsibilities:
- Read files
- Deserialize JSON

Non-responsibilities:
- Parsing
- Validation
- Business logic
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import orjson


class KnowledgeLoader:
    """Loads raw knowledge resources."""

    @staticmethod
    def load_json(path: str | Path) -> dict[str, Any]:
        """
        Load a JSON knowledge file.

        Args:
            path: Path to the JSON file.

        Returns:
            Parsed JSON as a dictionary.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the JSON is invalid.
        """

        file_path = Path(path)

        if not file_path.is_file():
            raise FileNotFoundError(
                f"Knowledge file not found: {file_path}"
            )

        try:
            return orjson.loads(file_path.read_bytes())

        except orjson.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON: {file_path}"
            ) from exc