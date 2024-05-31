import os
import unittest

from nthscraper.logger import setup_logger
from nthscraper.utils import FileUtils
from nthscraper.scraper import NthScraper

logger = setup_logger(log_file="", console_log=False)


class TestFileUtilsWrapper(unittest.TestCase):
    """Testing Requests Wrapper"""

    def test_utils_save_html(self):
        # test downloading using scraper
        scraper = NthScraper()
        scraper.get("https://httpbin.org")
        FileUtils().save_html(
            htmldir="./tests/downloads_test",
            filename="test_utils_save_html",
            scraper=scraper,
        )
        self.assertTrue(
            os.path.exists(
                os.path.abspath("./tests/downloads_test") + "/test_utils_save_html.html"
            )
        )

        # test downloading using url
        FileUtils().save_html(
            htmldir="./tests/downloads_test",
            filename="test_utils_save_html_url",
            url="https://httpbin.org",
        )

        self.assertTrue(
            os.path.exists(
                os.path.abspath("./tests/downloads_test")
                + "/test_utils_save_html_url.html"
            )
        )

        # test downloading body only data
        scraper.get_from_local(f"{os.path.abspath(os.path.curdir)}/tests/test.html")
        FileUtils().save_html(
            htmldir="./tests/downloads_test",
            filename="test_utils_save_html_body_only",
            scraper=scraper,
            body_only=True,
        )

        self.assertTrue(
            os.path.exists(
                os.path.abspath("./tests/downloads_test")
                + "/test_utils_save_html_body_only.html"
            )
        )

    def test_utils_download_file(self):
        """download a file"""
        FileUtils().download_file(
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "./tests/downloads_test",
            "pdf_download",
            "pdf",
        )

        self.assertTrue(
            os.path.exists(
                os.path.abspath("./tests/downloads_test") + "/pdf_download.pdf"
            )
        )
