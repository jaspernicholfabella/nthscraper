import unittest
import os
import requests
from zenscraper.wrapper.local_file_adapter import LocalFileAdapter
from zenscraper.scraper import ZenScraper
from zenscraper.by import By
from zenscraper.logger import setup_logger

logger = setup_logger(log_file="", console_log=False)


class TestLocalFileAdapter(unittest.TestCase):
    """check adapter for local files."""

    def test_local_file_adapter_get(self):
        """test to check if file local adapter works properly.
        testing if we can use request library on our local files.
        """
        file_path = os.path.abspath(os.path.curdir) + "/tests/test.html"
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
        scraper = self.scraper.get_from_local(f"{self.local_file_path}/tests/test.html")
        self.assertEqual(scraper.status_code, 200)

    def test_scraping_element(self):
        """Testing if element is properly extracted"""
        self.scraper.get_from_local(f"{self.local_file_path}/tests/test.html")
        element = self.scraper.find_element(By.XPATH, "//h2[@class='title']")
        self.assertIn("h2", str(element))

    def test_scraping_elements(self):
        """Testing if elements is properly extracted"""
        self.scraper.get_from_local(f"{self.local_file_path}/tests/test.html")
        elements = self.scraper.find_elements(By.XPATH, "//li//a")

        self.assertEqual(len(elements), 16)
        for element in elements:
            self.assertIn("<a>", str(element))


class TestZenElement(unittest.TestCase):

    def setUp(self):
        self.scraper = ZenScraper()
        self.local_file_path = os.path.abspath(os.path.curdir)
        self.scraper.get_from_local(f"{self.local_file_path}/tests/test.html")

    def test_element_get_values(self):
        """Testing to check if we are properly extracting text from an element"""
        element = self.scraper.find_element(By.XPATH, "//h2[@class='title']")
        self.assertEqual("Test Title title span", element.get_text().strip())
        self.assertEqual("Test Title", element.get_text(all_text_content=False).strip())
        self.assertEqual("h2", element.get_tag_name())

        # check for getting the parents
        element = self.scraper.find_element(By.XPATH, "//span[@class='title-span']")
        p = element.get_parent()
        self.assertEqual("h2", p.get_tag_name())

        # check for getting the children element
        elements = self.scraper.find_element(
            By.XPATH, "//div[@class='wrapper']"
        ).get_children()
        self.assertEqual(len(elements), 3)
        self.assertEqual("p", elements[0].get_tag_name())

    def test_finding_element_by_mode(self):
        """Test searching element by mode, XPATH will be skipped because it
        is heavily used in the initial tests, assuming it works properly
        """
        # By.ID
        element = self.scraper.find_element(By.ID, "sakalam")
        self.assertEqual("Malakas", element.get_text().strip())

        # By.CLASS_NAME
        element = self.scraper.find_element(By.CLASS_NAME, "wrapper")
        self.assertIn("!Wrapper Class", element.get_text().strip())

        # By.TAG_NAME
        elements = self.scraper.find_elements(By.TAG_NAME, "ol")
        self.assertEqual(len(elements), 2)
        for element in elements:
            self.assertEqual(element.get_text(), "ol")

        # By.LINK_TEXT
        elements = self.scraper.find_elements(By.LINK_TEXT, "Wrapper")
        self.assertEqual(len(elements), 4)
        for index, element in enumerate(elements):
            if index == 3:
                self.assertEqual(element.get_tag_name(), "a")
            else:
                self.assertEqual(element.get_tag_name(), "p")

        # By.TEXT
        element = self.scraper.find_element(By.TEXT, "Malakas")
        self.assertEqual(element.get_tag_name(), "p")
        self.assertEqual(element.get_attribute("id"), "sakalam")
