import os
import io
import sys
from typing import Tuple
from requests.adapters import BaseAdapter
from requests.models import Response
from urllib.request import url2pathname


class LocalFileAdapter(BaseAdapter):
    """Adapter for handling local file system paths."""

    def _chckpath(self, method: str, path: str) -> Tuple[int, str]:
        """Check the method and path, returning HTTP status codes and messages."""
        if method.lower() in ("put", "delete"):
            return 501, "Not Implemented"
        elif method.lower() not in ("get", "head"):
            return 405, "Method Not Allowed"
        elif os.path.isdir(path):
            return 400, "Path is a Directory"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """Emulate HTTP response from a local file."""

        if request.method is None or request.url is None:
            raise ValueError(
                "'Request method or URL in None, which is invalid HTTP Operations"
            )
        path = os.path.normcase(os.path.normpath(url2pathname(request.path_url)))
        response = Response()

        # Set initial response details
        response.status_code, response.reason = self._chckpath(request.method, path)
        response.url = request.url

        if response.status_code == 200 and request.method.lower() != "head":
            try:
                with open(path, "rb") as file_handle:
                    file_content = file_handle.read()
                response.raw = io.BytesIO(file_content)
            except Exception as e:
                response.status_code = 500
                response.reason = str(e)

        response.request = request
        return response

    def __enter__(self, *exc):
        return self
        logger.info(f"__exit__: {exc}")
        self.session.close()

    def close(self) -> None:
        """Implement close method if needed for cleaning up resources."""
        pass
