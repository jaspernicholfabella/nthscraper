import unittest
import glob
import os
import subprocess
from zenscraper.wrapper.etl_runner import Runner


class TestETLRunner(unittest.TestCase):

    def setUp(self):
        # delete final output before retesting
        self.file_path = "./tests/runner_test"
        subprocess.run(["rm", "-r", f"{self.file_path}/final/"])

    def test_etl_runner_output_csv(self):
        """test if etl_runner output csv working properly"""
        files = glob.glob(f"{self.file_path}/final/test_*.csv")
        self.assertFalse(files)

        subprocess.run(
            [
                "python",
                f"{self.file_path}/test.py",
                "-o",
                f"{self.file_path}/",
                "--outname",
                "test",
            ]
        )

        files = glob.glob("./tests/runner_test/final/test_*.csv")
        self.assertTrue(files)

    def test_etl_runner_output_json(self):
        """test if etl_runner output json working properly"""
        files = glob.glob(f"{self.file_path}/final/test_*.json")
        self.assertFalse(files)

        subprocess.run(
            [
                "python",
                f"{self.file_path}/test.py",
                "-o",
                f"{self.file_path}/",
                "--outtype",
                "json",
                "--outname",
                "test",
            ]
        )
        files = glob.glob("./tests/runner_test/final/test_*.json")
        self.assertTrue(files)

    def test_etl_runner_output_csv_with_index(self):
        files = glob.glob(f"{self.file_path}/final/test_*.csv")
        self.assertFalse(files)

        subprocess.run(
            [
                "python",
                f"{self.file_path}/test.py",
                "-o",
                f"{self.file_path}/",
                "--outname",
                "test",
                "-idx",
            ]
        )

        files = glob.glob("./tests/runner_test/final/test_*.csv")
        self.assertTrue(files)

    def test_etl_runner_output_csv_check_logs(self):
        """this is to test if logging works perfectly"""
        subprocess.run(["rm", "-r", f"{self.file_path}/logs/"])
        files = glob.glob(f"{self.file_path}/logs/test_*.log")
        self.assertFalse(files)

        subprocess.run(
            [
                "python",
                f"{self.file_path}/test.py",
                "-o",
                f"{self.file_path}/",
                "--outname",
                "test",
                "-idx",
                "-v",
                "--logfile",
                f"{self.file_path}/log/test_app.log",
            ],
        )

        files = glob.glob(f"{self.file_path}/logs/test_*.log")
        self.assertTrue(files)
