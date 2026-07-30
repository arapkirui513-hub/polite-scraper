# Polite Scraper Architecture

## Overview

The Polite Scraper is a modular Python application that collects web pages responsibly, extracts useful textual content, cleans and structures that content, and stores it as individual JSON documents suitable for Retrieval-Augmented Generation (RAG) or other downstream processing.

Each module has a single responsibility. The application is designed so that networking, parsing, extraction, cleaning, and storage remain independent components.

---

# High-Level Architecture

```
                config.yaml
                     │
                     ▼
               Configuration
                     │
                     ▼
                 main.py
                     │
                     ▼
              load_seed_urls()
                     │
                     ▼
               Fetcher.fetch()
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
   robots.txt   Rate limiting   HTTP GET
                     │
                     ▼
               requests.Response
                     │
                     ▼
                  Parser
                     │
                     ▼
               BeautifulSoup
                     │
                     ▼
                 Extractor
                     │
                     ▼
          {
            title,
            url,
            content
          }
                     │
                     ▼
                  Cleaner
                     │
                     ▼
            Cleaned document
                     │
                     ▼
                  Storage
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
  SHA-256 hash         Duplicate detection
          │
          ▼
     JSON document
```

---

# Component Responsibilities

## main.py

### Responsibilities

- Load application configuration.
- Configure logging.
- Load seed URLs.
- Coordinate the scraping pipeline.
- Report overall success and failure statistics.

### Does NOT

- Perform HTTP requests.
- Parse HTML.
- Clean extracted text.
- Save files directly.

---

## Fetcher

### Responsibilities

- Download web pages.
- Respect robots.txt rules.
- Apply crawl-delay where specified.
- Apply configurable minimum delay.
- Retry transient HTTP failures.
- Manage HTTP sessions.

### Does NOT

- Parse HTML.
- Extract article content.
- Store data.

---

## Parser

### Responsibilities

- Convert an HTTP response into a BeautifulSoup object.

### Does NOT

- Understand article structure.
- Clean text.
- Save output.

---

## Extractor

### Responsibilities

- Extract relevant article content.
- Preserve page title.
- Preserve source URL.

### Output

```python
{
    "title": "...",
    "url": "...",
    "content": "..."
}
```

---

## Cleaner

### Responsibilities

- Remove unnecessary whitespace.
- Remove citation markers.
- Normalize extracted text.

### Does NOT

- Modify page structure.
- Download content.

---

## Storage

### Responsibilities

- Generate metadata.
- Compute SHA-256 content hashes.
- Detect duplicate documents.
- Save JSON records.

### Does NOT

- Download data.
- Clean content.

---

# Data Flow

The scraper transforms data through several stages.

```
requests.Response
        │
        ▼
BeautifulSoup
        │
        ▼
Extracted dictionary
        │
        ▼
Cleaned dictionary
        │
        ▼
JSON document
```

Each stage produces a more structured representation than the previous one.

---

# Configuration

Application behaviour is controlled through `config.yaml`.

Configuration includes:

- Seed URL file
- Output directory
- Log file
- User-Agent
- Contact URL
- Minimum delay
- Timeout
- Retry count

Configuration is validated during application startup before scraping begins.

---

# Logging

The application uses Python's logging module.

Logs are written to:

- Console
- Configured log file

This provides a permanent execution record while preserving real-time console output.

---

# Storage Format

Each successfully scraped page is stored as an individual JSON document.

Each record contains:

- Unique identifier
- Title
- Source URL
- Category
- Cleaned content
- SHA-256 content hash
- Timestamp

Individual files simplify incremental updates, duplicate detection, and debugging.