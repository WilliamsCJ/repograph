"""
Utility functions for JSON parsing.
"""
import json
import logging
from typing import Dict, Any, Set, Tuple, List, Optional

JSONDict = Dict[str, Any]

log = logging.getLogger("repograph.utils.json")


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


def convert_dependencies_map_to_set(dependencies: List[JSONDict]) -> Set[str]:
    """Convert dependencies to a set of names.

    Args:
        dependencies (JSONDict): The JSONDict containing dependency information.

    Returns:
        Set[str]
    """
    converted = set()
    for dependency in dependencies:
        if "from_module" in dependency:
            converted.add(f"{dependency['from_module']}.{dependency['import']}")
        else:
            converted.add(dependency["import"])

    return converted
