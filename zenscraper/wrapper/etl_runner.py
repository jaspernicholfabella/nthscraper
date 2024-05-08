import time
import os
from datetime import datetime
import argparse
import pandas as pd
import logging
from typing import Any, List
from zenscraper.logger import setup_logger
from zenscraper.utils import ParserUtils, FileUtils


class Runner:
    """Class for data collection."""

    def __init__(
        self,
        argv: List[str],
        **kwargs: Any,
    ):
        self.args = self.parse_args(argv, **kwargs)

        console_log = False
        if self.args.verbose:
            console_log = True

        logging_level = logging.DEBUG
        logging_levels = [
            ("debug", logging.DEBUG),
            ("info", logging.INFO),
            ("warning", logging.WARNING),
            ("error", logging.ERROR),
        ]

        for levels in logging_levels:
            if self.args.loglevel == levels[0]:
                logging_level = levels[1]
                break

        self.outdir = self.args.outdir
        self.timestamp = datetime.now().strftime("%Y%m%d")
        self.prefix = f"{self.args.outname}_{self.timestamp}"

        log_file = ""
        if self.args.logfile:
            FileUtils().create_directory(f"{self.outdir}/logs")
            log_file = f"{self.outdir}/logs/{self.prefix}.log"

        self.logger = setup_logger(
            logging_level=logging_level, log_file=log_file, console_log=console_log
        )

        self.logger.info(f"logging_level: {logging_level}")
        self.logger.info(f"log_file: {log_file}")
        if console_log is True:
            self.logger.info(f"running on verbose")

        self.output_subdir = "/final/"

        if self.args.outtype:
            self.logger.info(f"Output Type: {self.args.outtype}")
            self.__output_type = self.args.outtype
        else:
            self.__output_type = "csv"

        self.__output_index = False
        if self.args.showindex:
            self.__output_index = True
        self.logger.info(f"Output Index: {self.__output_index}")

        self._argv = argv

    def run(self) -> pd.DataFrame:
        """Run the data collection process."""
        start_time = time.time()
        output_dir = os.path.abspath(f"{self.outdir}/{self.output_subdir}")
        FileUtils().create_directory(output_dir)

        self.logger.info("Starting data collection")
        raw_data = self.get_raw()
        normalized_data = self.normalize(raw_data)
        self.save_output(normalized_data)
        self.clean()

        elapsed_time = time.time() - start_time
        self.logger.info(f"Processed completed in {elapsed_time: .2f} seconds")
        return normalized_data

    def get_raw(self) -> Any:
        """Retrieve raw data. Must be implemented in subclasses."""
        raise NotImplementedError("Method get_raw() not implemented.")

    def normalize(self, raw_data: Any) -> pd.DataFrame:
        """Normalize raw data. Should be overridden by subclasses if necessary."""
        self.logger.info("Default normalization applied.")
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
        )
        if self.__output_type not in [method["type"] for method in output_methods]:
            raise UnsupportedOutputTypeException(self.__output_type)

        for val in output_methods:
            if val["type"] == self.__output_type:
                file_path = self._get_output_file(val["type"])
                if val["type"] == "json":
                    val["method"](file_path, orient="split", index=self.__output_index)
                else:
                    val["method"](file_path, index=self.__output_index)

    def parse_args(
        self, argv: List[str], description: str = "Collect data from website"
    ) -> argparse.Namespace:
        parser = ParserUtils().get_parser(description)
        parser.add_argument("--outname", help="Name of the output file")
        parser.add_argument("--outtype", help="Output type can either be [csv, json]")

        parser.add_argument(
            "-idx",
            "--showindex",
            action="store_true",
            help="Output index bool",
        )

        parser.add_argument(
            "--loglevel", help="specify log level [debug, info, warning, error]"
        )
        parser.add_argument("--logfile", action="store_true", help="generate log file")
        parser.add_argument(
            "-v", "--verbose", action="store_true", help="show logs on console bool"
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
            f"Unsupported output type: {output_type}. Supported types are [csv, json]."
        )


class ImplementationException(Exception):
    """Exception for unimplemented methods."""

    def __init__(self, method: str):
        super().__init__(f"Please implement {method}() in your subclass")
