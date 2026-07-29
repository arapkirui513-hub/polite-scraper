"""
Polite HTTP fetching.

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
    """Responsible for politely downloading web pages."""

    def __init__(
        self,
        user_agent: str,
        min_delay_seconds: float = 2.0,
        timeout_seconds: float = 10.0,
        max_retries: int = 3,
        contact_url: str | None = None,
    ):
        """
        Parameters
        ----------
        user_agent:
            Honest identifier for this scraper.

        min_delay_seconds:
            Minimum delay between requests to the same domain if robots.txt
            does not specify Crawl-delay.

        timeout_seconds:
            Maximum time to wait for an HTTP response.

        max_retries:
            Number of retries for transient HTTP failures.

        contact_url:
            Optional project or GitHub URL appended to the User-Agent.
        """

        full_agent = user_agent
        if contact_url:
            full_agent = f"{user_agent} (+{contact_url})"

        self.user_agent = full_agent
        self.min_delay_seconds = min_delay_seconds
        self.timeout_seconds = timeout_seconds

        self.robots = RobotsChecker(user_agent=full_agent)

        # Stores the timestamp of the last request per domain.
        self._last_request_time: dict[str, float] = {}

        # Persistent HTTP session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": full_agent})

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["GET"]),
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _domain(self, url: str) -> str:
        """Return the domain portion of a URL."""
        return urlparse(url).netloc

    def _wait_if_needed(self, url: str) -> None:
        """
        Respect Crawl-delay (if specified) or the configured minimum delay.
        """
        domain = self._domain(url)

        crawl_delay = self.robots.crawl_delay(url)
        required_delay = max(crawl_delay or 0.0, self.min_delay_seconds)

        last_request = self._last_request_time.get(domain)

        if last_request is None:
            return

        elapsed = time.monotonic() - last_request
        remaining = required_delay - elapsed

        if remaining > 0:
            logger.debug(
                "Rate limiting %s: sleeping %.2f seconds",
                domain,
                remaining,
            )
            time.sleep(remaining)

    def fetch(self, url: str) -> requests.Response | None:
        """
        Download a page while respecting robots.txt and rate limits.

        Returns
        -------
        requests.Response
            On success.

        None
            If the URL is disallowed or the request ultimately fails.
        """

        if not self.robots.can_fetch(url):
            logger.warning("Blocked by robots.txt: %s", url)
            return None

        self._wait_if_needed(url)

        try:
            response = self.session.get(
                url,
                timeout=self.timeout_seconds,
            )

            if response.history:
                logger.info(
                    "Redirected %s -> %s",
                    url,
                    response.url,
                )

            if response.ok:
                logger.info(
                    "Fetched %s (%d bytes)",
                    response.url,
                    len(response.content),
                )
                return response

            logger.warning(
                "HTTP %d returned for %s",
                response.status_code,
                response.url,
            )
            return None

        except requests.exceptions.Timeout:
            logger.error(
                "Timed out while fetching %s",
                url,
            )
            return None

        except requests.exceptions.RequestException as exc:
            logger.error(
                "Request failed for %s: %s",
                url,
                exc,
            )
            return None

        finally:
            # Always update the last request time so repeated failures
            # don't accidentally hammer the same server.
            self._last_request_time[self._domain(url)] = time.monotonic()

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()