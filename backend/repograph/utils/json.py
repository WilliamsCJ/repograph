"""
Utility functions for JSON parsing.
"""
import json
import logging
from typing import Dict, Any, Tuple, Optional

JSONDict = Dict[str, Any]

log = logging.getLogger("repograph.utils.json")


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
