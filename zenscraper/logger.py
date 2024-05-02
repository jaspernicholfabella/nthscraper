import logging
from logging.handlers import RotatingFileHandler


def setup_logger(logging_level=logging.DEBUG):
    """Set up and return a logger with a single instance across the app."""
    logger = logging.getLogger("my_app")
    if not logger.handlers:
        logger.setLevel(logging_level)
        # Create handlers
        f_handler = RotatingFileHandler(
            "app.log", maxBytes=1024 * 1024 * 5, backupCount=5
        )

        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(messages)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        f_handler.setFormatter(f_format)
        f_handler.setLevel(logging_level)

        logger.addHandler(f_handler)

    return logger
