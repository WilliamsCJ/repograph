"""
Utility functions for the build entity.
"""
# Base imports
import json
import os
from typing import Any, Dict, List, Union, Optional, Tuple, Set
from logging import getLogger
from pathlib import Path, PurePath

# pip imports
from requirements import parse
from requirements.requirement import Requirement

# Entity imports
from repograph.entities.graph.models.nodes import Class, Function, Module
from repograph.utils import JSONDict

# Logging
log = getLogger("repograph.entities.build.utils")


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


def find_node_object_by_name(
    nodes: List[Union[Class, Function, Module]],
    name: str,
    strict: bool = True,
) -> Optional[Union[Class, Function, Module]]:
    """Find a Node in a list of Nodes by name.

    Args:
        nodes (List[Union[Class, Function, Module]]): The list of Nodes.
        name (str): The name to filter by.
        strict (bool): Whether to log a warning if more than one result is found.

    Returns:
        Optional[Union[Class, Function, Module]]
    """
    # First check if there are any strict matches by canonical name
    filtered = [obj for obj in nodes if obj is not None and obj.canonical_name == name]

    # Next check if there are any matches by name
    if len(filtered) == 0:
        filtered = [obj for obj in nodes if obj is not None and obj.name == name]

    # Finally check that canonical components of the call are all contained in the canonical name
    # This is indicative of relative imports
    if len(filtered) == 0:
        filtered = [
            obj
            for obj in nodes
            if all(
                [
                    obj is not None
                    and part in (obj.canonical_name if obj.canonical_name else "")
                    for part in name.split(".")
                ]
            )
        ]

    if len(filtered) == 0:
        filtered = [
            obj for obj in nodes if obj is not None and name.split(".")[-1] == obj.name
        ]

    # If no matches, return None
    if len(filtered) == 0:
        return None

    # Warn if more than one result found
    if strict and len(filtered) > 1:
        log.warning("More than one result found! Returning first.")

    return filtered[0]


def find_requirements(path: str) -> List[Requirement]:
    """Find any Python requirements files at the or below the path provided

    Args:
        path (str): Path to start search at

    Returns:
        List[Requirement]
    """
    found = []

    for path in Path(path).rglob("requirements*.txt"):
        with open(path, "r") as fd:
            found.extend(parse(fd))

    return found


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


def is_root_folder(file_path: str) -> bool:
    """Checks file path to see if path represents the root of a repository.

    Args:
        file_path (str): Module path

    Returns:
        bool: Whether the path represents the root of the repository.
    """
    pure_path = PurePath(file_path)
    return len(pure_path.parts) == 1


def get_path_root(file_path: str) -> str:
    """Get the root of the supplied file path.

    Args:
        file_path (str): The file path to parse.

    Returns:
        str
    """

    pure_path = PurePath(file_path)
    return pure_path.parts[0]


def get_module_and_object_from_canonical_object_name(
    canonical_name: str,
) -> Tuple[Optional[str], str]:
    """Split out the canonical module name and object name from a
    canonical object name.

    Args:
        canonical_name (str): The canonical name of the object.

    Returns:
        str: The module canonical name
        str: The object name
    """
    parts = canonical_name.split(".")

    if len(parts) == 1:
        return None, canonical_name

    return ".".join(parts[:-1]), parts[-1]


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
