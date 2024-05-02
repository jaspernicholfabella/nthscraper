import os
from urllib.request import url2pathname
import random
import requests
from requests.models import Response
from lxml import html
from lxml.etree import _Element, tostring
from typing import Tuple, Optional, List, Any
from zenscraper.wrapper.requests_wrapper import RequestsWrapper
from zenscraper.wrapper.local_file_adapter import LocalFileAdapter


class ZenScraper:
    """class to scrape websites following selenium-like rules"""

    def __init__(self) -> None:
        self.requests_wrapper: RequestsWrapper = RequestsWrapper()
        self.doc = None
        self.response: Optional[Response] = None

    def _get_response(
        self,
        url: str,
        sleep_seconds: Optional[int] = None,
        is_post: bool = False,
        **kwargs: Any,
    ):
        sleep_seconds = (
            sleep_seconds if sleep_seconds is not None else random.randint(1, 5)
        )
        method = self.requests_wrapper.post if is_post else self.requests_wrapper.get
        self.response = method(url, sleep_seconds=sleep_seconds, **kwargs)
        self.doc = (
            html.fromstring(self.response.content) if self.response.content else None
        )
        return self.response

    def get(self, url: str, sleep_seconds: Optional[int] = None, **kwargs: Any):
        return self._get_response(url, sleep_seconds, **kwargs)

    def get_from_local(self, file_path: str) -> Response:
        session = requests.session()
        session.mount("file://", LocalFileAdapter())
        self.response = session.get(f"file://{file_path}")
        self.doc = (
            html.fromstring(self.response.content) if self.response.content else None
        )
        self.response.close()
        return self.response

    def post(self, url: str, sleep_seconds: Optional[int] = None, **kwargs: Any):
        return self._get_response(url, sleep_seconds, is_post=True, **kwargs)
