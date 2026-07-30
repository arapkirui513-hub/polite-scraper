# Future Roadmap

## Purpose

This document outlines potential future enhancements for the Polite Scraper. These items represent possible directions for the project rather than committed features.

The current implementation provides a solid foundation for responsible web scraping, modular processing, and structured data storage. Future work will focus on improving scalability, maintainability, and integration with downstream applications.

---

# Short-Term Goals

## Expand Test Coverage

Increase automated testing for all major components.

Areas to cover include:

- Fetcher
- Parser
- Extractor
- Cleaner
- Storage
- End-to-end pipeline execution

Comprehensive testing will improve confidence when introducing future changes.

---

## Improve Content Extraction

The current extractor focuses on Wikipedia article content.

Future improvements may include:

- Support for additional website layouts.
- More robust handling of missing elements.
- Configurable extraction strategies.

---

## Enhanced Error Reporting

Provide more informative logging for:

- HTTP failures
- robots.txt restrictions
- parsing errors
- storage failures

This will simplify troubleshooting and improve observability.

---

# Medium-Term Goals

## Database Storage

Replace file-based storage with a relational database such as PostgreSQL.

Potential benefits include:

- Faster duplicate detection
- Structured querying
- Better scalability
- Improved data integrity

JSON export can remain available for portability.

---

## Search and Indexing

Introduce indexing to support efficient document retrieval.

Possible approaches include:

- SQLite Full-Text Search (FTS)
- PostgreSQL Full-Text Search
- Dedicated search engines for larger datasets

---

## Docker Support

Package the application using Docker to simplify deployment and ensure consistent runtime environments.

Possible additions include:

- Dockerfile
- Docker Compose configuration
- Volume-based persistent storage

---

## Continuous Integration

Introduce automated workflows using GitHub Actions.

Potential checks include:

- Unit tests
- Linting
- Formatting validation
- Documentation checks

---

# Long-Term Vision

## Retrieval-Augmented Generation (RAG)

Use the scraper as a document ingestion pipeline for Retrieval-Augmented Generation systems.

Possible additions include:

- Document chunking
- Embedding generation
- Vector database integration
- Semantic search

---

## Multiple Content Sources

Extend support beyond a single website.

Potential additions include:

- News websites
- Technical documentation
- Public datasets
- Blogs
- Government publications

Support will continue to respect each site's robots.txt rules and usage policies.

---

## Incremental Crawling

Track previously scraped pages and download only content that has changed.

Potential techniques include:

- Content hashing
- Last-Modified headers
- ETag support

This would reduce unnecessary requests and improve efficiency.

---

## Monitoring and Metrics

Introduce operational metrics to better understand scraper performance.

Examples include:

- Pages processed
- Success rate
- Retry count
- Average response time
- Duplicate detection rate

These metrics could be integrated into dashboards or monitoring systems.

---

# Production Roadmap

A possible evolution of the project is shown below.

```
Current JSON Storage
        │
        ▼
Improved Test Coverage
        │
        ▼
Database Storage
        │
        ▼
Search & Indexing
        │
        ▼
Docker Deployment
        │
        ▼
Continuous Integration
        │
        ▼
RAG Integration
        │
        ▼
Monitoring & Metrics
```

Each stage builds upon the previous one, allowing the project to evolve incrementally while maintaining its modular architecture.

---

# Guiding Principles

Future development will continue to prioritise:

- Responsible web scraping
- Clear separation of responsibilities
- Maintainable architecture
- Configuration-driven behaviour
- Incremental improvement
- Comprehensive documentation

These principles have guided the current implementation and will continue to shape future iterations of the project.