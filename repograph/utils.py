"""
Utility functions.
"""
import json
import logging
import os
from pathlib import PurePath
from typing import Any, Dict, Optional, Tuple

"JSONDict type hint"
JSONDict = Dict[str, Any]


log = logging.getLogger("utils")


def read_json_from_file(file_path: str) -> Dict[str, Any]:
    """Reads a JSON object from a file.

    Args:
        file_path (str): The path of the file to read.

    Returns:
        Dict[str, Any]: The JSON object as a dictiontary.
    """
    with open(file_path, "r") as file:
        json_obj = json.load(file)
        return json_obj


def strip_file_path_prefix(file_path: str) -> str:
    """Strips the first part of a file_path.

    Args:
        file_path (str): File path to strip.

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
        file_path (str): File path

    Returns:
        bool: Whether the path represents the root of the repository.
    """
    pure_path = PurePath(file_path)
    return len(pure_path.parts) == 1


def sort_path(x):
    return int(os.path.splitext(os.path.basename(x))[0])


def get_path_root(file_path: str) -> str:
    pure_path = PurePath(file_path)
    return pure_path.parts[0]


def parse_min_max_line_numbers(json: JSONDict) -> Tuple[Optional[int], Optional[int]]:
    """Retrieve a tuple of minimum and maximum line numbers from
    the "min_max_lineno" JSON entry.

    Uses .get() to avoid KeyErrors.

    Args:
        json (JSONDict): The JSON dictionary.

    Returns:
        Tuple[Optional[int], Optional[int]]: _description_
    """
    min_max = json.get("min_max_lineno", None)
    if not min_max:
        return None, None

    return min_max.get("min_lineno", None), min_max.get("max_lineno", None)


def marshall_json_to_string(json_dict: JSONDict) -> Optional[str]:
    """Serialises a JSONDict to a str.

    Args:
        json_dict (JSONDict): The JSON to serialise.

    Returns:
        str, if serialisable. Otherwise None.
    """
    if not json_dict:
        return None
    else:
        try:
            return json.dumps(json_dict)
        except TypeError:
            log.error("Couldn't serialise JSON to string.")
            return None
