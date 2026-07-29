"""
HTML parser.

Converts an HTTP response into a BeautifulSoup object.

Responsibilities:
    - Validate the response.
    - Parse HTML with BeautifulSoup.
    - Return a BeautifulSoup document.

This module does NOT decide which content is important.
Content extraction belongs in extractor.py.
"""

import logging

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger("scraper.parser")


class Parser:
    """Parses HTML into a BeautifulSoup document."""

    @staticmethod
    def parse(response: requests.Response) -> BeautifulSoup | None:
        """
        Parse an HTTP response into a BeautifulSoup object.

        Parameters
        ----------
        response : requests.Response
            HTTP response returned by Fetcher.fetch().

        Returns
        -------
        BeautifulSoup
            Parsed HTML document.

        None
            If parsing fails.
        """
        if response is None:
            logger.warning("No response supplied to parser.")
            return None

        try:
            soup = BeautifulSoup(response.text, "lxml")

            logger.info(
                "Parsed HTML (%d characters)",
                len(response.text),
            )

            return soup

        except Exception as exc:
            logger.exception("Failed to parse HTML: %s", exc)
            return None