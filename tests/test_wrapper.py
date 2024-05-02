import unittest
from zenscraper.wrapper.requests_wrapper import RequestsWrapper


class TestRequestsWrapper(unittest.TestCase):
    """Testing Requests Wrapper"""

    def test_request_wrapper_get(self):
        request = RequestsWrapper()
        res = request.get("https://httpbin.org/", sleep_seconds=0)
        self.assertEqual(res.status_code, 200)

    def test_request_wrapper_post(self):
        request = RequestsWrapper()
        payload = {"id": [1, 2, 3], "userId": 1}
        res = request.post(
            "https://jsonplaceholder.typicode.com/posts/",
            params=payload,
            sleep_seconds=0,
        )
        self.assertEqual(res.status_code, 201)

    def test_request_wrapper_hit_count(self):
        with RequestsWrapper() as RW:
            RW.get("https://httpbin.org/", sleep_seconds=0)
            RW.get("https://httpbin.org/", sleep_seconds=0)
            self.assertEqual(RW.get_hit_count(), 2)


if __name__ == "__main__":
    unittest.main()
