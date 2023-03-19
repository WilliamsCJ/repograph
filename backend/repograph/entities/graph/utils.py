"""
Utility functions for the graph entity.
"""
# Base imports
from pathlib import PurePath
from logging import getLogger
from typing import Tuple

# Logging
log = getLogger("repograph.entities.graph.utils")


def get_path_name(file_path: str) -> str:
    """Gets the name of the file or directory pointed to by the file path.

    Args:
        file_path (str): The file path to find the name of.

    Returns:
        str: The name of the file or directory in the file path.
    """
    pure_path = PurePath(file_path)
    return pure_path.parts[-1]


def get_path_parent(file_path: str) -> str:
    """Gets the path of the parent for a given file_path.

    Args:
        file_path (str): The file path to find the parent of.

    Returns:
        str: Parent file path
    """
    pure_path = PurePath(file_path)
    return str(pure_path.parent)


def get_package_parent_and_name(package: str) -> Tuple[str, str]:
    """Get the package parent.

    Args:
        package (str): Package to parse.

    Returns:
        str: The parent package
        str: The package name
    """
    parts = package.split(".")

    if len(parts) == 1:
        return "", package

    return ".".join(parts[:-1]), parts[-1]
