"""
Storage module.

Adds metadata to cleaned records and saves them as JSON.
"""

import hashlib
import json
import logging
from datetime import datetime, UTC
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

logger = logging.getLogger("scraper.storage")


class Storage:
    """Save cleaned records to disk."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def content_hash(content: str) -> str:
        """
        Generate a SHA-256 hash of the cleaned content.
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def _category(url: str) -> str:
        """
        Infer the source category from the URL.
        """
        domain = urlparse(url).netloc.lower()

        if "wikipedia.org" in domain:
            return "wikipedia"

        return domain

    def save(self, record: dict | None) -> Path | None:
        """
        Save a cleaned record as a JSON document.

        Returns:
            Path to the saved JSON file, or None if saving failed.
        """
        if record is None:
            logger.warning("No record supplied for storage.")
            return None

        output = {
            "id": str(uuid4()),
            "title": record["title"],
            "url": record["url"],
            "category": self._category(record["url"]),
            "content": record["content"],
            "content_hash": self.content_hash(record["content"]),
            "scraped_at": datetime.now(UTC).isoformat(),
        }

        filename = f"{output['id']}.json"
        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                output,
                file,
                indent=2,
                ensure_ascii=False,
            )

        logger.info("Saved record to %s", filepath)

        return filepath