"""robots.txt compliance.

Every URL the scraper touches must be checked against its domain's
robots.txt before fetching. Rules are cached per domain so we fetch
robots.txt once per host, not once per page.
"""

import logging
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

logger = logging.getLogger("scraper.robots")


class RobotsChecker:
    """Caches and enforces robots.txt rules on a per-domain basis."""

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self._parsers: dict[str, RobotFileParser] = {}
        self._unreachable: set[str] = set()

    def _domain_key(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _get_parser(self, url: str) -> RobotFileParser | None:
        """Fetch and cache the robots.txt parser for a URL's domain.

        Returns None if robots.txt could not be retrieved. Per the
        robots.txt spec, a missing or unreachable robots.txt is treated
        as "no restrictions", but we log it clearly since that is a
        meaningful trust decision, not a silent default.
        """
        domain = self._domain_key(url)

        if domain in self._parsers:
            return self._parsers[domain]

        if domain in self._unreachable:
            return None

        robots_url = f"{domain}/robots.txt"
        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            parser.read()
            self._parsers[domain] = parser
            logger.info("Loaded robots.txt for %s", domain)
        except Exception as exc:
            logger.warning(
                "Could not fetch robots.txt for %s (%s). Treating as unrestricted per spec.",
                domain, exc,
            )
            self._unreachable.add(domain)
            return None

        return parser

    def can_fetch(self, url: str) -> bool:
        """Return True if this scraper's user agent is permitted to fetch url."""
        parser = self._get_parser(url)
        if parser is None:
            return True
        allowed = parser.can_fetch(self.user_agent, url)
        if not allowed:
            logger.info("Disallowed by robots.txt: %s", url)
        return allowed

    def crawl_delay(self, url: str) -> float | None:
        """Return the crawl-delay in seconds specified for this domain, if any."""
        parser = self._get_parser(url)
        if parser is None:
            return None
        delay = parser.crawl_delay(self.user_agent)
        return float(delay) if delay is not None else None
