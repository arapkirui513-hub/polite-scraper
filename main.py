"""
Main entry point for the Polite Scraper.

Pipeline:

seed_urls.txt
      │
      ▼
RobotsChecker
      ▼
Fetcher
      ▼
Parser
      ▼
Extractor
      ▼
Cleaner
      ▼
Storage
"""

import time
from pathlib import Path

from app.cleaner import Cleaner
from app.extractor import Extractor
from app.fetcher import Fetcher
from app.parser import Parser
from app.robots import RobotsChecker
from app.storage import Storage

USER_AGENT = "KevinKiruiPoliteScraper/1.0"
CONTACT_URL = "https://github.com/arapkirui513-hub/polite-scraper"

SEED_FILE = Path("data/seed_urls.txt")


def load_urls(filepath: Path) -> list[str]:
    """
    Load seed URLs from a text file.

    Ignores:
    - blank lines
    - comments beginning with #
    """
    if not filepath.exists():
        print(f"Seed file not found: {filepath}")
        return []

    urls = []

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            urls.append(line)

    return urls


def main():
    urls = load_urls(SEED_FILE)

    if not urls:
        print("No seed URLs found.")
        return

    robots = RobotsChecker(USER_AGENT)

    fetcher = Fetcher(
        user_agent=USER_AGENT,
        contact_url=CONTACT_URL,
    )

    storage = Storage()

    success = 0
    failed = 0

    try:
        for url in urls:

            print("\n" + "=" * 70)
            print(f"Processing: {url}")

            # Check robots.txt
            if not robots.can_fetch(url):
                print("Blocked by robots.txt")
                failed += 1
                continue

            # Respect crawl-delay if provided
            delay = robots.crawl_delay(url)

            if delay:
                print(f"Waiting {delay:.1f} seconds (crawl-delay)...")
                time.sleep(delay)

            # Fetch page
            response = fetcher.fetch(url)

            if response is None:
                print("Fetch failed.")
                failed += 1
                continue

            # Parse HTML
            soup = Parser.parse(response)

            if soup is None:
                print("Parse failed.")
                failed += 1
                continue

            # Extract article
            record = Extractor.extract(soup, url)

            if record is None:
                print("Extraction failed.")
                failed += 1
                continue

            # Clean text
            cleaned = Cleaner.clean(record)

            if cleaned is None:
                print("Cleaning failed.")
                failed += 1
                continue

            # Save JSON
            filepath = storage.save(cleaned)

            if filepath is None:
                print("Storage failed.")
                failed += 1
                continue

            print(f"Saved: {filepath}")
            success += 1

        print("\n" + "=" * 70)
        print("SCRAPING COMPLETE")
        print("=" * 70)
        print(f"Successful : {success}")
        print(f"Failed     : {failed}")
        print(f"Total      : {success + failed}")
        print("=" * 70)

    finally:
        fetcher.close()


if __name__ == "__main__":
    main()