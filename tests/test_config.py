import tempfile
import unittest
from pathlib import Path

from app.fetcher import Fetcher
from app.storage import Storage
from app.utils import load_config, load_seed_urls, setup_logging


class ConfigTests(unittest.TestCase):
    def test_load_config_reads_required_values(self):
        with self.subTest("custom config values"):
            with tempfile.TemporaryDirectory() as temp_dir:
                config_path = Path(temp_dir) / "config.yaml"
                config_path.write_text(
                    "\n".join(
                        [
                            'seed_urls_file: "data/custom_seeds.txt"',
                            'output_dir: "output_test"',
                            'log_file: "output/test.log"',
                            'user_agent: "ConfigTestBot/1.0"',
                            'contact_url: "https://example.com/contact"',
                            "min_delay_seconds: 5",
                            "timeout_seconds: 1",
                            "max_retries: 0",
                        ]
                    ),
                    encoding="utf-8",
                )

                config = load_config(str(config_path))

        self.assertEqual(config["seed_urls_file"], "data/custom_seeds.txt")
        self.assertEqual(config["output_dir"], "output_test")
        self.assertEqual(config["log_file"], "output/test.log")
        self.assertEqual(config["user_agent"], "ConfigTestBot/1.0")
        self.assertEqual(config["contact_url"], "https://example.com/contact")
        self.assertEqual(config["min_delay_seconds"], 5)
        self.assertEqual(config["timeout_seconds"], 1)
        self.assertEqual(config["max_retries"], 0)

    def test_load_config_requires_output_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config_path.write_text(
                "\n".join(
                    [
                        'seed_urls_file: "data/seed_urls.txt"',
                        'output_file: "output/corpus.json"',
                        'log_file: "output/scraper.log"',
                        'user_agent: "ConfigTestBot/1.0"',
                        'contact_url: "https://example.com/contact"',
                        "min_delay_seconds: 2",
                        "timeout_seconds: 10",
                        "max_retries: 3",
                    ]
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(KeyError, "output_dir"):
                load_config(str(config_path))

    def test_seed_urls_file_controls_loaded_urls(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            seed_file = Path(temp_dir) / "single_seed.txt"
            seed_file.write_text(
                "\n".join(
                    [
                        "# ignored comment",
                        "https://example.com/only-page",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            urls = load_seed_urls(str(seed_file))

        self.assertEqual(urls, ["https://example.com/only-page"])

    def test_output_dir_controls_storage_location(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "output_test"

            storage = Storage(output_dir=str(output_dir))

            self.assertEqual(storage.output_dir, output_dir)
            self.assertTrue(output_dir.is_dir())

    def test_log_file_controls_logging_location(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "output" / "test.log"

            logger = setup_logging(str(log_file))
            logger.info("configuration log path test")

            self.assertTrue(log_file.exists())
            self.assertIn(
                "configuration log path test",
                log_file.read_text(encoding="utf-8"),
            )

            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)

    def test_fetcher_uses_configured_user_agent_and_http_settings(self):
        fetcher = Fetcher(
            user_agent="ConfigTestBot/1.0",
            contact_url="https://example.com/contact",
            min_delay_seconds=5,
            timeout_seconds=1,
            max_retries=0,
        )

        try:
            expected_user_agent = "ConfigTestBot/1.0 (+https://example.com/contact)"

            self.assertEqual(fetcher.user_agent, expected_user_agent)
            self.assertEqual(fetcher.session.headers["User-Agent"], expected_user_agent)
            self.assertEqual(fetcher.robots.user_agent, expected_user_agent)
            self.assertEqual(fetcher.min_delay_seconds, 5)
            self.assertEqual(fetcher.timeout_seconds, 1)
        finally:
            fetcher.close()


if __name__ == "__main__":
    unittest.main()
