import unittest
import os
import requests
from zenscraper.wrapper.local_file_adapter import LocalFileAdapter


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


if __name__ == "__main__":
    unittest.main()
