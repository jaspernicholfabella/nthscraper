import unittest
from nthscraper.checkpoint import Checkpoint


class TestCheckpoint(unittest.TestCase):
    """Creating test cases for checkpoint"""

    def setUp(self):
        """setup checkpoint file."""
        self.checkpoint = Checkpoint(pickle_file="./tests/pickle_test/test.pickle")

    def test_checkpoint_save_and_load(self):
        """this is to test if in we want to save a data on our checkpoint
        we will check if the data will be loaded and saved"""
        data = "hello"
        self.checkpoint.save_data(data)
        self.assertTrue(self.checkpoint.exists)
        data = "hello3"

        self.assertEqual(data, "hello3")
        data = self.checkpoint.load_data()
        self.assertEqual(data, "hello")

    def test_checkpoint_save_and_load_urls(self):
        """this is to check if we are loading checkpoints properly (this is used
        mostly for url links)"""
        url_list = []
        for i in range(0, 10):
            url_list.append(f"webpage_{i}.com")

        self.checkpoint.save_checkpoint(url_list)

        new_url_list = []

        for url in url_list:
            if "5" in url:
                break
            new_url_list.append(url)

        url_list = self.checkpoint.load_checkpoint(new_url_list)
        for i in range(6, 10):
            self.assertNotIn(f"webpage_{i}.com", url_list)

        for i in range(0, 5):
            self.assertIn(f"webpage_{i}.com", url_list)
