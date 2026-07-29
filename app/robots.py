"""
robots.txt compliance.

Every URL the scraper touches must be checked against its domain's
robots.txt before fetching. Rules are cached per domain so we fetch
robots.txt once per host, not once per page.
"""

import logging
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests

logger = logging.getLogger("scraper.robots")


class RobotsChecker:
    """Caches and enforces robots.txt rules on a per-domain basis."""

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self._parsers: dict[str, RobotFileParser] = {}
        self._unreachable: set[str] = set()

    def _domain_key(self, url: str) -> str:
        """Return the scheme + domain for a URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _get_parser(self, url: str) -> RobotFileParser | None:
        """
        Fetch and cache the robots.txt parser for a URL's domain.

        Returns None if robots.txt cannot be retrieved. Following the
        robots.txt specification, an unreachable robots.txt is treated
        as unrestricted, but this is logged clearly.
        """
        domain = self._domain_key(url)

        # Return cached parser if available
        if domain in self._parsers:
            return self._parsers[domain]

        # Don't repeatedly retry unreachable robots.txt files
        if domain in self._unreachable:
            return None

        robots_url = f"{domain}/robots.txt"

        try:
            response = requests.get(
                robots_url,
                headers={"User-Agent": self.user_agent},
                timeout=10,
            )

            response.raise_for_status()

            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.parse(response.text.splitlines())

            self._parsers[domain] = parser

            logger.info("Loaded robots.txt for %s", domain)

            return parser

        except requests.RequestException as exc:
            logger.warning(
                "Could not fetch robots.txt for %s (%s). "
                "Treating as unrestricted per robots.txt specification.",
                domain,
                exc,
            )

            self._unreachable.add(domain)
            return None

    def can_fetch(self, url: str) -> bool:
        """
        Return True if this scraper's User-Agent is allowed
        to fetch the supplied URL.
        """
        parser = self._get_parser(url)

        if parser is None:
            return True

        allowed = parser.can_fetch(self.user_agent, url)

        if not allowed:
            logger.info("Disallowed by robots.txt: %s", url)

        return allowed

    def crawl_delay(self, url: str) -> float | None:
        """
        Return the crawl-delay specified in robots.txt, if present.
        """
        parser = self._get_parser(url)

        if parser is None:
            return None

        delay = parser.crawl_delay(self.user_agent)

        return float(delay) if delay is not None else None