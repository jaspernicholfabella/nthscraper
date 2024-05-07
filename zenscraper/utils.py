import os
import re
import glob
import json
import time
import pandas as pd
import argparse
import requests

from pathlib import Path
from typing import Optional, Union, List

from zenscraper.logger import setup_logger
from zenscraper.scraper import ZenScraper
from zenscraper.by import By
from zenscraper.wrapper.requests_wrapper import RequestsWrapper

logger = setup_logger()


class FileUtils:
    """File utilities"""

    def save_html(
        self,
        htmldir: str,
        filename: str,
        scraper: Optional[ZenScraper] = None,
        url: Optional[str] = None,
        body_only: bool = False,
    ):
        """
        Save HTML from a webpage source using zenscraper , or from a
        direct URL.
        """
        logger.info("Saving HTML Files")
        Path(os.path.abspath(htmldir)).mkdir(parents=True, exist_ok=True)

        def _extract_html(zs: ZenScraper):
            if body_only:
                body = zs.find_element(By.XPATH, "//body")
                out = f"<html><body>{body}</body></html>" if body is not None else ""
            else:
                out = zs.response.text if zs.response else ""
            return out

        if scraper is not None:
            output = _extract_html(scraper)
        elif url is not None:
            i_scraper = ZenScraper()
            i_scraper.get(url, sleep_seconds=0)
            output = _extract_html(i_scraper)

        file_path = os.path.join(os.path.abspath(htmldir), f"{filename}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)

    
    def save_json(self, 
                  jsondir:str,
                  filename: str,
                  jsondata:Optional[str] = None
                  url:str = "",
                  sleep_seconds_before: Optional[int] = None,
                  sleep_seconds_after: Optional[int] = None):
        """
        Save JSON data from a URL or provided JSON data to a file in the specified
        directory.

        :param jsondir: Directory to save the JSON file.
        :param filename: JSON Data from a string extracted
        :param url: URL to fetch JSON data
        :param sleep_seconds_before: Time to wait before making the request
        :param sleep_aeconds_after: Time to wait after the requeat is made before saving
        the file
        """
        logger.info("Saving JSON file")
        Path(os.path.abspath(jsondir)).mkdir(parents=True, exist_ok=True)
        json_output = b""

        if url:
            req = RequestsWrapper()
            res = req.get(
                url,
                sleep_seconds=(
                    sleep_seconds if sleep_seconds is not None else 0
                ),
            )
            time.sleep(wait_time)
            json_output = res.content
        elif json_data:
            json_output = str.encode(json.dumps(json_data, indent=4))

        file_path = Path(jsondir, f"{filename}.json")
        try:
            file_path.write_bytes(json_output)
            logger.info("JSON file saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save JSON file: {e}")

        
