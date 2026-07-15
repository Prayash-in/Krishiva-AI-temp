"""
Utility for constructing structured retrieval text.
"""

from __future__ import annotations


class TextBuilder:
    """Builds consistently formatted retrieval text."""

    def __init__(self) -> None:
        self._lines: list[str] = []

    # ---------------------------------------------------------
    # Sections
    # ---------------------------------------------------------

    def section(self, title: str) -> None:
        """Add a section heading."""

        self._lines.append(f"## {title}")
        self._lines.append("")

    # ---------------------------------------------------------
    # Paragraph
    # ---------------------------------------------------------

    def text(self, value: str | None) -> None:
        """Add a paragraph."""

        if not value:
            return

        self._lines.append(value.strip())
        self._lines.append("")

    # ---------------------------------------------------------
    # List
    # ---------------------------------------------------------

    def bullets(self, values: list[str]) -> None:
        """Add a bullet list."""

        if not values:
            return

        for value in values:
            self._lines.append(f"- {value}")

        self._lines.append("")

    # ---------------------------------------------------------
    # Multilingual List
    # ---------------------------------------------------------

    def multilingual_bullets(
        self,
        values: dict[str, list[str]],
        language: str = "en",
    ) -> None:
        """Render phrases from one language."""

        phrases = values.get(language, [])

        self.bullets(phrases)

    # ---------------------------------------------------------
    # Key-Value
    # ---------------------------------------------------------

    def field(
        self,
        key: str,
        value: str | None,
    ) -> None:
        """Add a single key-value pair."""

        if value:

            self._lines.append(f"{key}: {value}")

    # ---------------------------------------------------------
    # Build
    # ---------------------------------------------------------

    def build(self) -> str:
        """Return final retrieval text."""

        return "\n".join(self._lines).strip()
    
    def key_value_group(
        self,
        groups: dict[str, dict],
    ) -> None:
        """
        Render nested key-value dictionaries.

        Example:
        {
            "first_choice": {
                "fungicide": "...",
                "dose": "...",
            },
            "second_choice": {
               ...
            }
        }
        """

        if not groups:
            return

        for group_name, values in groups.items():

            self._lines.append(
                f"### {group_name.replace('_', ' ').title()}"
            )

            if not isinstance(values, dict):
                self._lines.append(str(values))
                self._lines.append("")
                continue

            for key, value in values.items():

                if value in (None, "", [], {}):
                    continue

                if isinstance(value, list):

                    if all(isinstance(item, dict) for item in value):
                        self.list_of_objects(value)
                        continue

                    self.bullets([str(item) for item in value])
                    continue

                self._lines.append(
                    f"{key.replace('_', ' ').title()}: {value}"
                )

            self._lines.append("")

    def key_value(
     self,
        values: dict,
    ) -> None:
        """
        Render a flat dictionary.

        Example:
        {
            "infection_cycle": "...",
            "survival": "...",
        }
        """

        if not values:
            return

        for key, value in values.items():

            if value in (None, "", [], {}):
                continue

            self._lines.append(
                f"### {key.replace('_', ' ').title()}"
            )

            if isinstance(value, list):
                self.bullets(value)

            else:
                self.text(str(value))

    def list_of_objects(
        self,
        objects: list[dict],
    ) -> None:
        """
        Render a list of dictionaries.
        """

        if not objects:
            return

        for index, obj in enumerate(objects, start=1):

            title = obj.get(
                "type",
                f"Item {index}"
            )

            self._lines.append(f"### {title.replace('_', ' ').title()}")

            for key, value in obj.items():

                if key == "type":
                    continue

                if isinstance(value, list):

                    self._lines.append(
                        key.replace("_", " ").title()
                    )

                    self.bullets(value)

                else:

                    self._lines.append(
                        f"{key.replace('_',' ').title()}: {value}"
                    )

            self._lines.append("")   