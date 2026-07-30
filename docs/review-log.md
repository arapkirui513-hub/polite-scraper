# Review Log

## Purpose

This document records significant reviews, observations, and improvements made during the development of the Polite Scraper.

Unlike the changelog, which focuses on released features, this log captures the reasoning behind architectural refinements and code quality improvements.

---

# Review 1 – Initial Implementation

## Summary

The first working version successfully scraped web pages, extracted content, and stored results as JSON files.

The project demonstrated the complete scraping pipeline but included several areas that could be improved for maintainability and scalability.

## Observations

- Networking behaviour was distributed across multiple files.
- Configuration values were partially hard-coded.
- Duplicate documents could be written multiple times.
- Documentation focused primarily on implementation rather than design.

## Actions Taken

- Planned refactoring into clearer module responsibilities.
- Identified opportunities for centralised configuration.
- Began improving project documentation.

---

# Review 2 – Architecture Refactoring

## Summary

The application was reorganised to improve separation of concerns and reduce duplicated logic.

## Improvements

### Networking

- Consolidated HTTP requests, robots.txt handling, retries, and request timing inside the `Fetcher`.

### Configuration

- Moved runtime settings into `config.yaml`.
- Added configuration validation during application startup.

### Storage

- Introduced SHA-256 content hashing.
- Added duplicate detection before writing JSON files.

### Documentation

Created dedicated documentation for:

- architecture
- design decisions
- lessons learned
- roadmap
- changelog

---

# Review 3 – Repository Cleanup

## Summary

The repository was simplified by removing obsolete files and improving organisation.

## Improvements

### Removed

- Unused configuration modules.
- Legacy debugging scripts.
- Obsolete dependencies.
- Redundant documentation.

### Verified

- Configuration is loaded from a single source.
- Networking responsibilities remain isolated within the `Fetcher`.
- Documentation reflects the current architecture.

---

# Current Status

## Strengths

- Modular architecture.
- Centralised configuration.
- Responsible scraping behaviour.
- Duplicate detection.
- Structured project documentation.
- Clear separation of responsibilities.

## Remaining Opportunities

Future work includes:

- Expand automated test coverage.
- Improve extraction rules for additional websites.
- Add database-backed storage.
- Introduce continuous integration.
- Add performance metrics and monitoring.

---

# Lessons from Review

Several themes emerged throughout development:

- Small, focused modules are easier to maintain.
- Centralised configuration reduces maintenance overhead.
- Early validation prevents difficult runtime failures.
- Documentation should explain design decisions, not just implementation.
- Incremental refactoring is safer than large-scale rewrites.

These reviews helped shape the project into a cleaner, more maintainable, and more extensible application.