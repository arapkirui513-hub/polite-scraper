"""
Storage module.

Adds metadata to cleaned records, prevents duplicate content,
and saves records as JSON.
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

    def _find_duplicate(self, content_hash: str) -> Path | None:
        """
        Return the path of an existing record with the same content hash,
        or None if no duplicate exists.
        """
        for file in self.output_dir.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    existing = json.load(f)

                if existing.get("content_hash") == content_hash:
                    return file

            except (json.JSONDecodeError, OSError):
                logger.warning("Could not read %s", file)

        return None

    def save(self, record: dict | None) -> Path | None:
        """
        Save a cleaned record as JSON.

        If an identical record already exists (same content hash),
        return the existing file instead of creating a duplicate.
        """
        if record is None:
            logger.warning("No record supplied for storage.")
            return None

        content_hash = self.content_hash(record["content"])

        duplicate = self._find_duplicate(content_hash)

        if duplicate is not None:
            logger.info("Duplicate detected. Using existing file: %s", duplicate)
            return duplicate

        output = {
            "id": str(uuid4()),
            "title": record["title"],
            "url": record["url"],
            "category": self._category(record["url"]),
            "content": record["content"],
            "content_hash": content_hash,
            "scraped_at": datetime.now(UTC).isoformat(),
        }

        filename = f"{output['id']}.json"
        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                output,
                f,
                indent=2,
                ensure_ascii=False,
            )

        logger.info("Saved record to %s", filepath)

        return filepath