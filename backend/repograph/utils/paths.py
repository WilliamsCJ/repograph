"""
Utility functions for handling file paths.
"""
import os
import logging
from pathlib import PurePath
from typing import Tuple


log = logging.getLogger("repograph.utils.paths")


def strip_file_path_prefix(file_path: str) -> str:
    """Strips the first part of a file_path.

    Args:
        file_path (str): Module path to strip.

    Returns:
        str: The stripped file path.
    """
    pure_path = PurePath(file_path)
    pure_path = PurePath("/".join(pure_path.parts[1:]))
    return str(pure_path)


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


def is_root_folder(file_path: str) -> bool:
    """Checks file path to see if path represents the root of a repository.

    Args:
        file_path (str): Module path

    Returns:
        bool: Whether the path represents the root of the repository.
    """
    pure_path = PurePath(file_path)
    return len(pure_path.parts) == 1


def sort_path(x) -> int:
    """Sorts a list of paths names hierarchically.

    Args:
        x:

    Returns:

    """
    return int(os.path.splitext(os.path.basename(x))[0])


def get_path_root(file_path: str) -> str:
    """Get the root of the supplied file path.

    Args:
        file_path (str): The file path to parse.

    Returns:
        str
    """

    pure_path = PurePath(file_path)
    return pure_path.parts[0]


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


def get_canonical_package_root_and_child(package: str) -> Tuple[str, str]:
    """Retrieve the root package and child canonical package from a
    canonical package name.

    Args:
        package (str): The package to parse.

    Returns:
        str: The root package
        str: The child package name
    """
    parts = package.split(".")

    if len(parts) == 1:
        return package, ""

    return parts[0], ".".join(parts[1:])
