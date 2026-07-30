# Design Decisions

## Purpose

This document explains the key architectural decisions made during the development of the Polite Scraper. Where appropriate, it also describes alternatives that were considered and the reasons they were not chosen.

---

# 1. Modular Pipeline Architecture

## Decision

Split the scraper into independent modules:

- Fetcher
- Parser
- Extractor
- Cleaner
- Storage

## Why

Each stage has a single responsibility, making the system easier to understand, maintain, and extend.

For example:

- Improvements to text cleaning do not affect networking.
- Storage changes do not require modifications to the parser.
- Extraction logic can evolve independently of the HTTP client.

## Alternative

Place all scraping logic in a single script.

## Why Not

A monolithic implementation becomes difficult to maintain as additional features—such as retries, duplicate detection, or new extraction rules—are introduced.

---

# 2. Centralised Configuration

## Decision

Store application settings in `config.yaml`.

Configuration includes:

- User-Agent
- Contact URL
- Output directory
- Seed URL file
- Retry count
- Timeout
- Crawl delay

## Why

Configuration changes should not require source code modifications.

Separating configuration from implementation makes the scraper easier to deploy in different environments and simplifies future automation.

## Alternative

Hard-code values inside the application.

## Why Not

Hard-coded values increase maintenance effort and make experimentation more difficult.

---

# 3. Fetcher Owns Networking

## Decision

The `Fetcher` component is responsible for:

- HTTP requests
- robots.txt compliance
- Retry handling
- Rate limiting
- Request timing

## Why

Keeping all networking concerns in one component prevents duplicated logic and ensures every request follows the same behaviour.

## Alternative

Handle robots.txt checks and delays inside `main.py`.

## Why Not

Networking behaviour would become scattered across multiple files, making future changes harder to implement consistently.

---

# 4. One JSON File per Record

## Decision

Store each scraped document as an individual JSON file.

## Why

Individual files provide several advantages:

- Incremental updates without rewriting an entire corpus.
- Simpler duplicate detection.
- Easier debugging of individual records.
- Straightforward inspection during development.

## Alternative

Store all documents in a single `corpus.json` file.

## Why Not

A single file grows continually, requires rewriting on every update, and makes duplicate handling more complex.

---

# 5. SHA-256 Duplicate Detection

## Decision

Generate a SHA-256 hash from the cleaned document content before saving.

## Why

Content hashes provide a reliable way to identify duplicate documents regardless of filename or scrape time.

This approach also avoids storing the same article multiple times when the scraper is run repeatedly.

## Alternative

Compare URLs only.

## Why Not

Different URLs may reference identical content, while the same URL may change over time.

---

# 6. Configuration Validation

## Decision

Validate required configuration values during application startup.

## Why

Failing early prevents runtime errors caused by missing or incomplete configuration.

Users receive immediate feedback if required settings are absent.

## Alternative

Allow missing configuration values and rely on defaults.

## Why Not

Hidden defaults can make application behaviour unpredictable and more difficult to debug.

---

# 7. Logging Instead of Print Statements

## Decision

Use Python's `logging` module throughout the application.

## Why

Logging provides:

- configurable verbosity,
- timestamps,
- persistent execution records,
- simultaneous console and file output.

This approach is more appropriate for production software than ad hoc print statements.

## Alternative

Use `print()` for status messages.

## Why Not

Print statements are difficult to manage as applications grow and cannot easily be filtered or redirected.

---

# 8. Seed URL File

## Decision

Read starting URLs from `seed_urls.txt`.

## Why

Separating input data from application logic makes it easy to modify scrape targets without editing code.

## Alternative

Embed URLs directly inside `main.py`.

## Why Not

Embedding URLs couples application logic with project data and makes the scraper less reusable.

---

# Trade-offs

Every design decision involves trade-offs.

Current priorities favour:

- readability,
- maintainability,
- responsible web scraping,
- modularity,
- ease of extension.

These choices occasionally sacrifice raw performance—for example, duplicate detection currently scans existing JSON files—but they provide a simpler implementation that is appropriate for a project of this scale.

Future iterations may replace some of these approaches with more scalable solutions, such as indexed storage or relational databases.

---

# Future Evolution

The current architecture is intended as a foundation rather than a finished product.

Potential future enhancements include:

- PostgreSQL-backed storage.
- Full-text indexing.
- Docker deployment.
- Automated testing expansion.
- Continuous integration.
- Metrics and monitoring.
- Retrieval-Augmented Generation (RAG) integration.

The modular design allows these improvements to be introduced with minimal changes to existing components.