"""Utility functions for filtering"""
import logging
from typing import List, Optional, Union

from repograph.entities.graph.models.nodes import Module, Class, Function

log = logging.getLogger("repograph.utils.nodes")


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

    # If no matches, return None
    if len(filtered) == 0:
        return None

    # Warn if more than one result found
    if strict and len(filtered) > 1:
        log.warning("More than one result found! Returning first.")

    return filtered[0]
