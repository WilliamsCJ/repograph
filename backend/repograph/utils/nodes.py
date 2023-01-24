"""Utility functions for filtering"""
import logging
from typing import List, Optional, Union

from repograph.models.nodes import Module, Class, Function

log = logging.getLogger("repograph.utils.nodes")


def find_node_object_by_name(
        nodes: List[Union[Class, Function, Module]],
        name: str,
        strict: bool = True,
        canonical: bool = False
) -> Optional[Union[Class, Function, Module]]:
    """Find a Node in a list of Nodes by name.

    Args:
        nodes (List[Union[Class, Function, Module]]): The list of Nodes.
        name (str): The name to filter by.
        strict (bool): Whether to log a warning if more than one result is found.
        canonical (bool): Whether to use canonical name.

    Returns:
        Optional[Union[Class, Function, Module]]
    """
    if canonical:
        filtered = [obj for obj in nodes if obj is not None and obj.canonical_name == name]
    else:
        filtered = [obj for obj in nodes if obj is not None and obj.name == name]

    if len(filtered) == 0:
        return None

    if strict and len(filtered) > 1:
        log.warning("More than one result found! Returning first.")

    return filtered[0]
