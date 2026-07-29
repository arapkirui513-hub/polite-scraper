"""Logging setup and configuration loading."""

import logging
import sys
from pathlib import Path

import yaml


def setup_logging(log_file: str = "output/scraper.log", level: int = logging.INFO) -> logging.Logger:
    """Configure a logger that writes to both console and a log file.

    Called once at startup. All modules should use logging.getLogger(__name__)
    to get a child logger rather than reconfiguring logging themselves.
    """
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("scraper")
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def load_config(config_path: str = "config.yaml") -> dict:
    """Load the scraper configuration from a YAML file.

    Raises FileNotFoundError with a clear message rather than letting
    a cryptic yaml parse error surface, since a missing config is the
    most common first-run mistake.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found at '{config_path}'. "
            f"Copy config.example.yaml to config.yaml and edit it first."
        )
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config or {}


def load_seed_urls(seed_file: str) -> list[str]:
    """Load seed URLs from a plain text file, one URL per line.

    Blank lines and lines starting with # are ignored so the seed file
    can carry comments explaining why each URL was included.
    """
    path = Path(seed_file)
    if not path.exists():
        raise FileNotFoundError(f"Seed URL file not found at '{seed_file}'.")

    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls
