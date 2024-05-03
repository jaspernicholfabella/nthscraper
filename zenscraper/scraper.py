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
from zenscraper.by import By, selector_mode_values
from zenscraper.logger import setup_logger

logger = setup_logger()


class ZenElement:
    """Represents an HTML element in the Zenscraper context."""

    def __init__(self, element: _Element):
        if not isinstance(element, _Element):
            raise ValueError("Expected an lxml.etree._Element instance.")
        self.element: _Element = element

    def find_elements(
        self, by_mode: "By", to_search: str, tag: str = "node()"
    ) -> List["ZenElement"]:
        """Find multiple elemnts within this element."""
        err_message, xpath = selector_mode_values(by_mode, to_search, tag)
        try:
            elements = self.element.xpath(xpath)
            return [ZenElement(element) for element in elements] if elements else []
        except Exception:
            logger.error(f"{err_message}: {e}")
            return []

    def find_element(self, by_mode: "By", to_search: str) -> "ZenElement":
        """
        Attempt to find an HTML element by XPATH or other methods and return it wrapped in a ZenElement
        """
        _, xpath = selector_mode_values(by_mode, to_search)
        try:
            element = self.element.xpath(xpath)[0]
        except Exception:
            raise ValueError("Failed to find element.")
        return ZenElement(element)

    def get_text(self) -> str:
        """Retrieve the combined text content of the HTML element."""
        return "".join(self.element.itertext())

    def inner_html(self) -> str:
        """Get the inner HTML of the element."""
        return tostring(self.element, encoding="unicode", method="html")

    def get_tag_name(self) -> str:
        """Get the tag name of the element."""
        return self.element.tag

    def __str__(self):
        """Representation of ZenElement object."""
        return f"ZenElement: <{self.get_tag_name()}> element instance."


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
        logger.info(f"Scraping data from: {file_path}")
        self.doc = (
            html.fromstring(self.response.content) if self.response.content else None
        )
        self.response.close()
        return self.response

    def post(self, url: str, sleep_seconds: Optional[int] = None, **kwargs: Any):
        return self._get_response(url, sleep_seconds, is_post=True, **kwargs)

    def find_elements(
        self,
        by_mode: "By",
        to_search: str,
        doc: Optional[html.HtmlElement] = None,
        tag: str = "node()",
    ) -> List["ZenElement"]:
        err_message, xpath = selector_mode_values(by_mode, to_search, tag)
        doc = doc if doc else self.doc

        if doc is None or len(doc) == 0:
            logger.error("Document is not loaded properly for xpath operations.")
            return []
        try:
            elements = doc.xpath(xpath)
            return [ZenElement(element) for element in elements] if elements else []
        except Exception as e:
            logger.error(f"{err_message}: {e}")
            return []

    def find_element(
        self,
        by_mode: "By",
        to_search: str,
        doc: Optional[html.HtmlElement] = None,
        tag: str = "node()",
    ) -> "ZenElement":
        err_message, xpath = selector_mode_values(by_mode, to_search, tag)
        doc = doc if doc else self.doc
        if doc is None or len(doc) == 0:
            raise ReferenceError("HTML Document is not a valid lxml object")
        try:
            element = doc.xpath(xpath)[0]
            return ZenElement(element)
        except Exception:
            raise ValueError("Failed to find Element")

        return ZenElement(element)
