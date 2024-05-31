import logging
from logging.handlers import RotatingFileHandler


def setup_logger(logging_level=logging.DEBUG, log_file="", console_log=True):
    """Set up and return a logger."""
    logger = logging.getLogger("zenscraper")
    logger.setLevel(logging_level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add file handler if log file is provided
    if log_file:
        f_handler = RotatingFileHandler(
            log_file, maxBytes=1024 * 1024 * 5, backupCount=5
        )
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    # Add console handler if console_log is True
    if console_log:
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter("%(levelname)s - %(message)s")
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

    return logger
