"""
Models representing elements of the Repograph
"""
# base imports
from typing import List

# pip imports
from pydantic import BaseModel


class GraphSummary(BaseModel):
    """
    GraphSummary represents a summary about a Repograph.

    Args:
        is_empty (bool): Whether the graph is empty.
        nodes_total (int): Total number of nodes in the graph.
        relationships_total (int): Total number of relationships in the graph.
        repositories (int): Number of repositories contained in the graph.
        classes (int): Number of classes contained in the graph.
        functions (int): Number of functions contained in the graph.
        modules (int): Number of modules contained in the graph.
        packages (int): Number of packages contained in the graph.

    """
    is_empty: bool = True
    nodes_total: int = True
    relationships_total: int = True
    repositories: int = 0
    classes: int = 0
    functions: int = 0
    modules: int = 0
    packages: int = 0


class CallGraph(BaseModel):
    class Function(BaseModel):
        id: int
        label: str
        title: str

    class Relationship(BaseModel):
        from_id: int
        to_id: int

    nodes: List[Function] = []
    edges: List[Relationship] = []
