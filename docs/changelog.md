# Changelog

All notable changes to the Polite Scraper project are documented in this file.

The format is inspired by *Keep a Changelog* and follows semantic versioning where practical.

---

## [Unreleased]

### Planned

- Expand automated test coverage.
- Add PostgreSQL storage backend.
- Introduce Docker support.
- Implement continuous integration.
- Improve content extraction for additional websites.
- Add search and indexing capabilities.
- Explore Retrieval-Augmented Generation (RAG) integration.

---

## [1.2.0]

### Added

- Dedicated project documentation under the `docs/` directory.
- Architecture documentation.
- Design decisions documentation.
- Future roadmap.
- Lessons learned.
- Project review log.
- Changelog.

### Improved

- Documentation structure and cross-referencing.
- Separation between implementation, design, and project history.

---

## [1.1.0]

### Added

- Configuration validation during application startup.
- SHA-256 content hashing.
- Duplicate document detection.
- Centralised configuration using `config.yaml`.

### Changed

- Refactored networking responsibilities into the `Fetcher`.
- Improved logging configuration.
- Simplified application orchestration in `main.py`.

### Removed

- Legacy debugging scripts.
- Obsolete configuration module.
- Redundant project dependencies.

---

## [1.0.0]

### Initial Release

Initial implementation of the Polite Scraper featuring:

- Modular scraping pipeline.
- robots.txt compliance.
- Configurable request delays.
- Retry handling.
- HTML parsing with BeautifulSoup.
- Article content extraction.
- Text cleaning.
- JSON document storage.
- Logging support.