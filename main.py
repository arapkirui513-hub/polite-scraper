"""
Main entry point for the Polite Scraper.
"""

from app.cleaner import Cleaner
from app.extractor import Extractor
from app.fetcher import Fetcher
from app.parser import Parser
from app.storage import Storage
from app.utils import (
    load_config,
    load_seed_urls,
    setup_logging,
)


def main():
    """Run the scraping pipeline."""

    config = load_config()

    logger = setup_logging(config["log_file"])

    urls = load_seed_urls(config["seed_urls_file"])

    if not urls:
        logger.warning("No seed URLs found.")
        return

    fetcher = Fetcher(
        user_agent=config["user_agent"],
        min_delay_seconds=config["min_delay_seconds"],
        timeout_seconds=config["timeout_seconds"],
        max_retries=config["max_retries"],
        contact_url=config["contact_url"],
    )

    storage = Storage(
        output_dir=config["output_dir"],
    )

    success = 0
    failed = 0

    try:
        for url in urls:
            logger.info("=" * 70)
            logger.info("Processing %s", url)

            response = fetcher.fetch(url)

            if response is None:
                logger.warning("Fetch failed: %s", url)
                failed += 1
                continue

            soup = Parser.parse(response)

            if soup is None:
                logger.warning("Parse failed: %s", url)
                failed += 1
                continue

            record = Extractor.extract(soup, url)

            if record is None:
                logger.warning("Extraction failed: %s", url)
                failed += 1
                continue

            cleaned = Cleaner.clean(record)

            if cleaned is None:
                logger.warning("Cleaning failed: %s", url)
                failed += 1
                continue

            filepath = storage.save(cleaned)

            if filepath is None:
                logger.warning("Storage failed: %s", url)
                failed += 1
                continue

            logger.info("Stored: %s", filepath)
            success += 1

    finally:
        fetcher.close()

    logger.info("=" * 70)
    logger.info("SCRAPING COMPLETE")
    logger.info("=" * 70)
    logger.info("Successful: %s", success)
    logger.info("Failed: %s", failed)
    logger.info("Total: %s", success + failed)
    logger.info("=" * 70)


if __name__ == "__main__":
    main()