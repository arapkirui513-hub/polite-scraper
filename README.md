# Polite Scraper

A Python web scraper that collects pages responsibly, extracts useful content, cleans it, and saves structured records for use as a Retrieval-Augmented Generation (RAG) corpus.

## Features

- Respects robots.txt
- Uses a descriptive User-Agent
- Rate limiting
- Structured JSON output
- Built with Python, Requests, and BeautifulSoup

# Polite Scraper

## Features

- robots.txt compliance
- Custom User-Agent
- Crawl-delay support
- HTML parsing with BeautifulSoup
- Article extraction
- Text cleaning
- JSON storage
- SHA-256 content hashing

## Project Structure

app/
    robots.py
    fetcher.py
    parser.py
    extractor.py
    cleaner.py
    storage.py

main.py

## Run

python main.py