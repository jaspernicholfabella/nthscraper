import time
import os
from pathlib import Path
from datetime import datetime
import argparse
import pandas as pd
from typing import Any, Optional, List
from zenscraper.logger import setup_logger
from zenscraper.utils import ParserUtils

logger = setup_logger()


class Runner:
    """Class for data collection."""

    def __init__(
        self,
        argv: List[str],
        **kwargs: Any,
    ):
        self.args = self.parse_args(argv, **kwargs)
        self.outdir = self.args.outdir
        self.timestamp = datetime.now().strftime("%Y%m%d")
        self.prefix = f"{self.args.outname}_{self.timestamp}"
        self.output_subdir = "/final/"
        self.__output_type = self.args.outtype or "csv"

        if self.args.outindex == "True".lower():
            self.__output_index = True
        else:
            self.__output_index = False
        self._argv = argv

    def run(self) -> pd.DataFrame:
        """Run the data collection process."""
        start_time = time.time()
        output_dir = Path(os.path.abspath(f"{self.outdir}/{self.output_subdir}"))
        output_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Starting data collection")
        raw_data = self.get_raw()
        normalized_data = self.normalize(raw_data)
        self.save_output(normalized_data)
        self.clean()

        elapsed_time = time.time() - start_time
        logger.info(f"Processed completed in {elapsed_time: .2f} seconds")
        return normalized_data

    def get_raw(self) -> Any:
        """Retrieve raw data. Must be implemented in subclasses."""
        raise NotImplementedError("Method get_raw() not implemented.")

    def normalize(self, raw_data: Any) -> pd.DataFrame:
        """Normalize raw data. Should be overridden by subclasses if necessary."""
        logger.info("Default normalization applied.")
        return pd.DataFrame(raw_data)

    def _get_output_file(self, extension: str) -> str:
        """Construct output file path based on current settings."""
        return os.path.abspath(
            f"{self.outdir}/{self.output_subdir}/{self.prefix}.{extension}"
        )

    def save_output(self, data: pd.DataFrame) -> None:
        """Saved normalized data based on specified output type."""
        output_methods = (
            {"type": "csv", "method": data.to_csv},
            {"type": "json", "method": data.to_json},
            {"type": "excel", "method": data.to_excel},
        )

        if self.__output_type not in output_methods:
            raise UnsupportedOutputTypeException(self.__output_type)

        for val in output_methods:
            file_path = self._get_output_file(val["type"])
            if val["type"] == "json":
                val["method"](file_path, orient="split", index=self.__output_index)
            else:
                val["method"](file_path, index=self.__output_index)

    def parse_args(
        self, argv: List[str], description: str = "Collect data from website"
    ) -> argparse.Namespace:
        parser = ParserUtils().get_parser(description)
        parser.add_argument("-on", "--outname", help="Name of the output file")
        parser.add_argument(
            "-ot", "--outtype", help="Output type can either be [csv, json, excel]"
        )

        parser.add_argument(
            "-idx",
            "--outindex",
            help="Output index if index should be shown on the output (True or False)",
        )

        parser.add_argument("--to", help="Send output to email group")
        parser.add_argument("--cc", help="CC output to email group")

        args, _ = parser.parse_known_args(argv[1:])
        return args

    def clean(self):
        """Clean remaining data"""


class UnsupportedOutputTypeException(Exception):
    """Exception for unsupported file output types."""

    def __init__(self, output_type: str):
        super().__init__(
            f"Unsupported output type: {output_type}. Supported types are [csv, json, excel]."
        )


class ImplementationException(Exception):
    """Exception for unimplemented methods."""

    def __init__(self, method: str):
        super().__init__(f"Please implement {method}() in your subclass")
