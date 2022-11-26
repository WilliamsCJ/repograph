"""
Logging utilities
"""
import logging
import sys


def configure_logging():
    """Configures logging for repograph.

    Modified code from: https://docs.python.org/3/howto/logging-cookbook.html

    Returns:
        None
    """
    # Configure root logger
    logger = logging.getLogger("repograph")
    logger.setLevel(logging.INFO)

    # Create file handler to capture all logs to file
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)

    # Create stream handler to display logs to stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setStream(stream=sys.stdout)

    # Format logs
    formatter = logging.Formatter('%(levelname)s:%(name)s | %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
