"""Polite HTTP fetching.

Wraps requests with:
  - an honest, identifying User-Agent
  - per-domain rate limiting (respects robots.txt crawl-delay when present,
    otherwise falls back to a configured minimum delay)
  - retry with exponential backoff on transient failures
  - timeout handling
  - a hard robots.txt check before every request

This module never bypasses RobotsChecker. If a URL is disallowed, fetch()
returns None and logs the reason rather than raising, so a single blocked
URL doesn't crash a batch run.
"""

import logging
import time
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.robots import RobotsChecker

logger = logging.getLogger("scraper.fetcher")


class Fetcher:
    def __init__(
        self,
        user_agent: str,
        min_delay_seconds: float = 2.0,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        contact_url: str | None = None,
    ):
        """
        user_agent: identifies this scraper honestly, e.g. "KevoPortfolioBot/1.0"
        min_delay_seconds: floor delay between requests to the same domain
            when robots.txt specifies no crawl-delay. If robots.txt specifies
            a longer crawl-delay, that value wins.
        contact_url: optional URL included in the User-Agent string so a
            site operator can identify and contact the bot's owner. This is
            expected practice for a "polite" scraper, not optional flavor.
        """
        full_agent = user_agent
        if contact_url:
            full_agent = f"{user_agent} (+{contact_url})"

        self.user_agent = full_agent
        self.min_delay_seconds = min_delay_seconds
        self.timeout_seconds = timeout_seconds
        self.robots = RobotsChecker(user_agent=full_agent)

        self._last_request_time: dict[str, float] = {}

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": full_agent})

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _domain(self, url: str) -> str:
        return urlparse(url).netloc

    def _wait_if_needed(self, url: str) -> None:
        """Enforce the delay between consecutive requests to the same domain."""
        domain = self._domain(url)

        crawl_delay = self.robots.crawl_delay(url)
        required_delay = max(crawl_delay or 0.0, self.min_delay_seconds)

        last_time = self._last_request_time.get(domain)
        if last_time is not None:
            elapsed = time.monotonic() - last_time
            remaining = required_delay - elapsed
            if remaining > 0:
                logger.debug("Rate limiting %s: sleeping %.2fs", domain, remaining)
                time.sleep(remaining)

    def fetch(self, url: str) -> requests.Response | None:
        """Fetch a URL, respecting robots.txt and rate limits.

        Returns the Response on success, or None if the URL was disallowed
        or the request failed after retries. Callers should treat None as
        "skip this URL" rather than a fatal error.
        """
        if not self.robots.can_fetch(url):
            logger.warning("Skipping disallowed URL: %s", url)
            return None

        self._wait_if_needed(url)

        try:
            response = self.session.get(url, timeout=self.timeout_seconds)
            self._last_request_time[self._domain(url)] = time.monotonic()

            if response.status_code == 200:
                logger.info("Fetched %s (%d bytes)", url, len(response.content))
                return response

            logger.warning("Non-200 response for %s: HTTP %d", url, response.status_code)
            return None

        except requests.exceptions.Timeout:
            logger.error("Timeout fetching %s after retries", url)
            return None
        except requests.exceptions.RequestException as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return None
