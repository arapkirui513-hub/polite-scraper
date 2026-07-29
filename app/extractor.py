"""
Content extraction.

Extracts the meaningful content from a parsed HTML document.
The extractor does not clean text or save data—it simply pulls
out the information we care about.
"""

import logging
from bs4 import BeautifulSoup

logger = logging.getLogger("scraper.extractor")


class Extractor:
    """Extract structured content from a BeautifulSoup document."""

    @staticmethod
    def extract(soup: BeautifulSoup, url: str) -> dict | None:
        """
        Extract the page title and article content.

        Args:
            soup: Parsed BeautifulSoup document.
            url: Original page URL.

        Returns:
            {
                "title": str,
                "url": str,
                "content": str
            }

        Returns None if extraction fails.
        """
        if soup is None:
            logger.warning("Cannot extract from an empty document.")
            return None

        # Remove unwanted elements
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        # Extract page title
        title = (
            soup.title.get_text(strip=True)
            if soup.title
            else "Untitled"
        )

        # Locate the main content area
        article = (
            soup.find("main")
            or soup.find("article")
            or soup.find(id="mw-content-text")
            or soup.body
        )

        if article is None:
            logger.warning("No article body found for %s", url)
            return None

        paragraphs = []

        for paragraph in article.find_all("p"):
            text = " ".join(paragraph.stripped_strings)

            if text:
                paragraphs.append(text)

        content = "\n\n".join(paragraphs)

        logger.info(
            "Extracted %d paragraphs from '%s'",
            len(paragraphs),
            title,
        )

        return {
            "title": title,
            "url": url,
            "content": content,
        }