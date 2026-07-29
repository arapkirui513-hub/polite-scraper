"""Tests for RobotsChecker. Uses a fixed robots.txt body so this runs
without live network access.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.robots import RobotsChecker

SAMPLE_ROBOTS_TXT = """
User-agent: *
Disallow: /private/
Crawl-delay: 5

User-agent: BadBot
Disallow: /
""".strip().splitlines()


def make_checker_with_fixed_rules():
    checker = RobotsChecker(user_agent="KevoPortfolioBot/1.0")
    # Bypass the network fetch in _get_parser by pre-populating the cache
    # with a parser built from an in-memory robots.txt body.
    from urllib.robotparser import RobotFileParser
    parser = RobotFileParser()
    parser.parse(SAMPLE_ROBOTS_TXT)
    checker._parsers["https://example.com"] = parser
    return checker


def test_allowed_path_is_permitted():
    checker = make_checker_with_fixed_rules()
    assert checker.can_fetch("https://example.com/wiki/Some_Article") is True


def test_disallowed_path_is_blocked():
    checker = make_checker_with_fixed_rules()
    assert checker.can_fetch("https://example.com/private/secret") is False


def test_crawl_delay_is_read_correctly():
    checker = make_checker_with_fixed_rules()
    assert checker.crawl_delay("https://example.com/wiki/Some_Article") == 5.0


def test_unreachable_robots_txt_defaults_to_allowed():
    checker = RobotsChecker(user_agent="KevoPortfolioBot/1.0")
    checker._unreachable.add("https://unreachable-domain.example")
    assert checker.can_fetch("https://unreachable-domain.example/page") is True


if __name__ == "__main__":
    test_allowed_path_is_permitted()
    test_disallowed_path_is_blocked()
    test_crawl_delay_is_read_correctly()
    test_unreachable_robots_txt_defaults_to_allowed()
    print("All robots.py tests passed.")
