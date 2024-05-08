import unittest
from zenscraper.wrapper.requests_wrapper import RequestsWrapper
from zenscraper.logger import setup_logger
from zenscraper.wrapper.row import Row

logger = setup_logger(log_file="", console_log=False)


class TestRequestsWrapper(unittest.TestCase):
    """Testing Requests Wrapper"""

    def test_request_wrapper_get(self):
        """Requests Wrapper get request"""
        request = RequestsWrapper()
        res = request.get("https://httpbin.org/", sleep_seconds=0)
        self.assertEqual(res.status_code, 200)

    def test_request_wrapper_post(self):
        """Test requests wrapper post requests"""
        request = RequestsWrapper()
        payload = {"id": [1, 2, 3], "userId": 1}
        res = request.post(
            "https://jsonplaceholder.typicode.com/posts/",
            params=payload,
            sleep_seconds=0,
        )
        self.assertEqual(res.status_code, 201)

    def test_request_wrapper_hit_count(self):
        """test request wrapper web hit count"""
        with RequestsWrapper() as RW:
            RW.get("https://httpbin.org/", sleep_seconds=0)
            RW.get("https://httpbin.org/", sleep_seconds=0)
            self.assertEqual(RW.get_hit_count(), 2)


class TestRow(unittest.TestCase):
    """Testing Row class for creating row fields"""

    def setUp(self):
        header = ["Field Value", "Test Field", "testField2"]
        self.row = Row(header)

    def test_row_header(self):
        """test if header are working properly"""
        self.assertEqual(["Field Value", "Test Field", "testField2"], self.row.header)
        self.assertEqual(["field_value", "test_field", "testfield2"], self.row._fields)

    def test_row_values(self):
        """test wether row values are appending properly"""
        values = ["field_value", "test_field_value", "test_field_2_value"]
        self.row.field_value = values[0]
        self.row.test_field = values[1]
        self.row.testfield2 = values[2]

        self.assertEqual(self.row.field_value.value, values[0])
        self.assertEqual(self.row.test_field.value, values[1])
        self.assertEqual(self.row.testfield2.value, values[2])

        self.assertTrue(len(self.row.values) == 3)
        self.assertEqual(self.row.values, values)

    def test_row_compute_key(self):
        "test if compute key works, generate hash based on value"
        header = ["Value", "ObjectKey"]
        self.row = Row(header)
        self.row.value = "Value"
        self.row.objectkey = self.row.compute_key()
        objectkey = "4a2b279bde333533a033c334f6b2dcbc7ff492a005e075b133072b0c2b40289b"
        self.assertEqual(self.row.objectkey.value, objectkey)
