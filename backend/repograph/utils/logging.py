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

    # Create stream handler to display logs to stdout
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setStream(stream=sys.stdout)

    # Format logs
    formatter = logging.Formatter('%(levelname)s:%(name)s | %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
