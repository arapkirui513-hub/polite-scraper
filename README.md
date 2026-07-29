# Polite Scraper

A Python web scraper that collects web pages responsibly, extracts useful content, cleans and structures the text, and stores it as a Retrieval-Augmented Generation (RAG) corpus.

The scraper follows responsible web scraping practices by respecting `robots.txt`, identifying itself with a descriptive User-Agent, and applying rate limiting between requests.

---

## Features

- Respects `robots.txt`
- Descriptive User-Agent with contact URL
- Crawl-delay support and configurable rate limiting
- Retry handling with configurable timeout
- HTML parsing using BeautifulSoup
- Article content extraction
- Text cleaning and normalization
- Duplicate detection using SHA-256 content hashing
- Structured JSON document storage
- Configuration-driven design using `config.yaml`
- Centralized logging to console and file
- Unit tests for configuration loading

---

## Project Structure

```
polite-scraper/
│
├── app/
│   ├── cleaner.py
│   ├── extractor.py
│   ├── fetcher.py
│   ├── parser.py
│   ├── robots.py
│   ├── storage.py
│   └── utils.py
│
├── data/
│   └── seed_urls.txt
│
├── output/
│
├── tests/
│   ├── test_config.py
│   └── test_robots.py
│
├── config.yaml
├── main.py
└── README.md
```

---

## Configuration

The scraper is configured through `config.yaml`.

Example settings include:

- Seed URL file
- Output directory
- Log file
- User-Agent
- Contact URL
- Minimum crawl delay
- Request timeout
- Maximum retries

Configuration is validated during startup to ensure all required settings are present.

---

## How It Works

```
Seed URLs
    ↓
Fetcher
    ↓
Parser
    ↓
Extractor
    ↓
Cleaner
    ↓
Storage
```

The fetcher:

- checks `robots.txt`
- respects crawl-delay
- applies rate limiting
- retries transient failures
- downloads the page

The storage module computes a SHA-256 hash of each document and prevents duplicate records from being written.

---

## Running the Project

Create and activate a virtual environment, install the required dependencies, then run:

```bash
python main.py
```

---

## Output

Each successfully scraped page is stored as an individual JSON document containing metadata such as:

- ID
- Title
- URL
- Category
- Cleaned content
- SHA-256 content hash
- Scrape timestamp

Logs are written to both the console and the configured log file.

---

## Technologies

- Python 3
- Requests
- BeautifulSoup4
- PyYAML