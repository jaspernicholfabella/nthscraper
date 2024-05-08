import sys
import os
import pandas as pd
from datetime import datetime
from typing import Any


from zenscraper.wrapper.row import Row
from zenscraper.wrapper.etl_runner import Runner
from zenscraper.scraper import ZenScraper
from zenscraper.by import By
from zenscraper.logger import setup_logger

logger = setup_logger()


class TestRunner(Runner):
    """Sample ETL process using Runner"""

    def __init__(self, argv):
        super().__init__(argv)
        header = ["Fetch Date", "Sample Data"]
        self.out = Row(header)
        self.fetch_out = []
        self.fetch_date = datetime.strptime("01/02/2023", "%d/%m/%Y").strftime(
            "%Y/%m/%d"
        )

    def get_raw(self):
        """Get raw data from source"""
        logger.info("Getting the raw")
        scraper = ZenScraper()
        scraper.get_from_local(f"{os.path.abspath('./tests/test.html')}")
        element = scraper.find_element(By.XPATH, "//h2")
        self.out.fetch_date = self.fetch_date
        self.out.sample_data = element.get_attribute("innerText")
        self.fetch_out.append(self.out.values)
        return self.fetch_out

    def normalize(self, raw_data: Any):
        """Save raw data to file"""
        data_frame = pd.DataFrame(raw_data, columns=self.out.header)
        data_frame.replace(
            to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"],
            value=["", ""],
            regex=True,
            inplace=True,
        )

        return data_frame

    def clean(self):
        pass


def main(argv):
    """Main Entry"""
    web = TestRunner(argv)
    web.run()


if __name__ == "__main__":
    main(sys.argv)
