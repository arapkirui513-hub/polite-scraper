"""
Text cleaning.

Cleans extracted text by removing citation markers, fixing spacing,
repairing merged words, and normalising whitespace. This module
operates only on plain text.
"""

import logging
import re

logger = logging.getLogger("scraper.cleaner")


class Cleaner:
    """Clean extracted article text."""

    @staticmethod
    def clean(record: dict | None) -> dict | None:
        """
        Clean an extracted record.

        Args:
            record: Dictionary containing title, url and content.

        Returns:
            Cleaned record, or None if input is invalid.
        """
        if record is None:
            logger.warning("No record supplied for cleaning.")
            return None

        content = record.get("content", "")

        # Remove Wikipedia citation markers like [1], [23]
        content = re.sub(r"\[\s*\d+\s*\]", "", content)

        # Remove spaces before punctuation
        # Example: "Kenya ." -> "Kenya."
        content = re.sub(r"\s+([.,;:!?])", r"\1", content)

        # Repair merged words where a lowercase letter is immediately
        # followed by an uppercase letter.
        # Examples:
        #   BritishKenya -> British Kenya
        #   theUnity -> the Unity
        #   ofHealth -> of Health
        content = re.sub(r"([a-z])([A-Z])", r"\1 \2", content)

        # Collapse multiple spaces and tabs into one space
        content = re.sub(r"[ \t]+", " ", content)

        # Collapse repeated blank lines while preserving paragraphs
        content = re.sub(r"\n\s*\n+", "\n\n", content)

        # Remove leading/trailing whitespace
        content = content.strip()

        cleaned = record.copy()
        cleaned["content"] = content

        logger.info("Cleaned article '%s'", cleaned["title"])

        return cleaned