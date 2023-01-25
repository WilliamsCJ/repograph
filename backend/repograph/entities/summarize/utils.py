"""
Code summarization utilities.
"""
import re


def clean_source_code(source_code: str) -> str:
    """Remove docstrings from source_code

    Args:
        source_code (str): The source code to clean.

    Returns:
        str: Cleaned source_code
    """
    return re.sub("(?s)\"\"\".*\"\"\"\n", "", source_code)
