import os
import argparse
import requests

from pathlib import Path
from typing import Optional

from zenscraper.logger import setup_logger
from zenscraper.scraper import ZenScraper
from zenscraper.by import By

logger = setup_logger()


class FileUtils:
    """File utilities"""

    @staticmethod
    def create_directory(dir_name: str):
        """Create a directory"""
        if os.path.exists(Path(dir_name)):
            pass
        else:
            logger.info(f"creating directory: {dir_name}")
            Path(dir_name).mkdir(parents=True, exist_ok=True)

    def save_html(
        self,
        htmldir: str,
        filename: str,
        scraper: Optional[ZenScraper] = None,
        url: Optional[str] = None,
        body_only: bool = False,
    ):
        """
        Save HTML from a webpage source using zenscraper , or from a
        direct URL.
        """
        logger.info("Saving HTML Files")
        FileUtils().create_directory(htmldir)

        def _extract_html(zs: ZenScraper):
            if body_only:
                body = zs.find_element(By.XPATH, "//body")
                out = f"<html><body>{body}</body></html>" if body is not None else ""
            else:
                out = zs.response.text if zs.response else ""
            return out

        if scraper is not None:
            output = _extract_html(scraper)
        elif url is not None:
            i_scraper = ZenScraper()
            i_scraper.get(url, sleep_seconds=0)
            output = _extract_html(i_scraper)

        file_path = os.path.join(os.path.abspath(htmldir), f"{filename}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output)

    def download_file(
        self,
        url: str,
        filedir: str = "",
        filename: str = "download",
        filetype: str = "txt",
        prefix: str = "",
    ):
        """
        Download a file from a URL and save it to a specified directory with a given
        filename and filetype
        """
        # Build the full file path
        file_path = Path(filedir) / f"{prefix}{filename}.{filetype}"

        # Check if the file already exists
        if file_path.exists():
            logger.warning(f"File already exists: {file_path}. Skipping download.")
            return

        # Proceed with the download
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            logger.info(f"Downloading from: {url}")
            FileUtils().create_directory(filedir)
            with open(file_path, "wb") as out_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        out_file.write(chunk)
            logger.info(f"Download success! File saved to {file_path}")
        else:
            logger.error(
                f"Failed to download file, URL returned status code: {response.status_code}"
            )


class ParserUtils:

    @staticmethod
    def check_dir_writable(outdir, exception=Exception) -> str:
        """Return the outdir if it is writable, otherwise raise an exception"""
        FileUtils().create_directory(f"{outdir}/raw")
        if os.path.isdir(outdir) and os.access(outdir, os.W_OK):
            return outdir
        raise exception(f"{outdir} is not writable or does not exist")

    def get_parser(
        self,
        description="Collect data from websites",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    ):
        """Create a common parer for input arguments"""
        parser = argparse.ArgumentParser(
            description=description, formatter_class=formatter_class
        )

        parser.add_argument(
            "-r", "--run", action="store_true", help="Run the whole process"
        )

        parser.add_argument(
            "-o",
            "--outdir",
            type=self.check_dir_writable,
            help="Output directory to store the results",
            required=True,
        )
        return parser


class EmailUtils:
    def send_email(self, to, subject, body=None, files=None, cc=None):
        """
        Send email with attachment
        msg = send_email(getpass.getuser(),)
        """
        pass
