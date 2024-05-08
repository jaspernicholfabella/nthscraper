"""Requests Wrapper for the zenscraper library"""

import time
import random
import requests
from typing import Any
from zenscraper.logger import setup_logger


logger = setup_logger()


class RequestsWrapper:
    web_hit_count = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    ]

    def __init__(self, **kwargs: Any):
        self.session = requests.Session()
        self.session.headers.update(kwargs)

    def request(self, method: str, url: str, **kwargs: Any):
        """
        Wrap requests.request().
        """
        sleep_seconds = kwargs.pop("sleep_seconds", random.randrange(1, 4))
        time.sleep(float(sleep_seconds))

        # Update headers with user-defined headers, if any
        headers = kwargs.pop("headers", {})

        # Randomly select a user agent
        headers["User-Agent"] = random.choice(self.user_agents)

        self.web_hit_count += 1
        resp = self.session.request(method, url, headers=headers, **kwargs)
        logger.info(f"Response: status_code={resp.status_code}")
        logger.info(f"headers={resp.request.headers}")
        logger.info(f"web_hit_count={self.web_hit_count}")
        resp.raise_for_status()
        return resp

    def get(self, url: str, **kwargs: Any):
        """Send a GET Request"""
        logger.info(f"GET from: url={url}, kwargs={kwargs}")
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any):
        """Send a POST request"""
        logger.info(f"POST from: url={url}, kwargs={kwargs}")
        return self.request("POST", url, **kwargs)

    def get_hit_count(self):
        """Return the current web hit count."""
        return self.web_hit_count

    def test_connection(self):
        """Test method to print a success message."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        logger.info("__exit__: %s", exc)
        self.session.close()
