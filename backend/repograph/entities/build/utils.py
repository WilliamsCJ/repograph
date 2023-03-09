"""
Utility functions for the build entity.
"""
# Base imports
import json
import os
from typing import Any, Dict, List, Union, Optional
from logging import getLogger
from pathlib import Path

# pip imports
from requirements import parse
from requirements.requirement import Requirement

# Entity imports
from repograph.entities.graph.models.nodes import Class, Function, Module

# Logging
log = getLogger("repograph.entities.build.service")


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
