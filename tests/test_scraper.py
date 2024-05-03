import unittest
import os
import requests
from zenscraper.wrapper.local_file_adapter import LocalFileAdapter
from zenscraper.scraper import ZenScraper
from zenscraper.by import By
from zenscraper.logger import setup_logger

logger = setup_logger(file_log="", console_log=False)


class TestLocalFileAdapter(unittest.TestCase):
    """check adapter for local files."""

    def test_local_file_adapter_get(self):
        """test to check if file local adapter works properly.
        testing if we can use request library on our local files.
        """
        file_path = os.path.abspath(os.path.curdir) + "/tests/httpbin.html"
        print("FILE PATH:", file_path)
        session = requests.session()
        session.mount("file://", LocalFileAdapter())
        res = session.get(f"file://{file_path}")
        self.assertEqual(res.status_code, 200)


class TestZenScraper(unittest.TestCase):
    """tests to check scraping on a website"""

    def setUp(self):
        self.scraper = ZenScraper()
        self.local_file_path = os.path.abspath(os.path.curdir)

    def test_scraping_online_site(self):
        """testing getting response from online site"""
        scraper = self.scraper.get("https://httpbin.org", sleep_seconds=1)
        self.assertEqual(scraper.status_code, 200)

        payload = {"key": "value"}
        scraper = self.scraper.post(
            "https://httpbin.org/post", data=payload, sleep_seconds=1
        )
        self.assertEqual(scraper.status_code, 200)

    def test_scraping_offline_site(self):
        """testing getting response from downloaded file"""
        scraper = self.scraper.get_from_local(
            f"{self.local_file_path}/tests/httpbin.html"
        )
        self.assertEqual(scraper.status_code, 200)

    def test_scraping_element(self):
        """Testing if element is properly extracted"""
        self.scraper.get_from_local(f"{self.local_file_path}/tests/httpbin.html")
        element = self.scraper.find_element(By.XPATH, "//h2[@class='title']")
        self.assertIn("h2", str(element))

    def test_scraping_elements(self):
        """Testing if elements is properly extracted"""
        self.scraper.get_from_local(f"{self.local_file_path}/tests/httpbin.html")
        elements = self.scraper.find_elements(By.XPATH, "//div//a")

        self.assertEqual(len(elements), 15)
        for element in elements:
            self.assertIn("<a>", str(element))


class TestZenElement(unittest.TestCase):

    def setUp(self):
        self.scraper = ZenScraper()
        self.local_file_path = os.path.abspath(os.path.curdir)
        self.scraper.get_from(local(f"{self.local_file_path}/tests/httpbin.html"))


if __name__ == "__main__":
    unittest.main()
