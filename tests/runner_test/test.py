import sys
import pandas as pd
from datetime import datetime

from zenscraper import Row
from zenscraper.wrapper.etl_runner import Runner


class TestRunner(Runner):
    """Sample ETL process using Runner"""

    def __init__(self, argv):
        super().__init__(argv)
        header = ["Fetch Date", "Sample Data"]
        self.out = Row(header)
