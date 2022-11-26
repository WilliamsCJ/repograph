"""
This module defines the Repograph class and the operations/queries that can be performed on it
"""

from typing import List

from backend.repograph.models.graph import GraphSummary
from backend.repograph.neo4j import Neo4JDatabase


class Repograph(Neo4JDatabase):
    database: str
    node_types: List[str] = [
        "Class",
        "Function"
    ]

    def __init__(self, uri, user, password, database) -> None:
        super().__init__(uri, user, password, database)

    def get_summary(self) -> GraphSummary:
        if not self.has_nodes():
            return GraphSummary()

        summary = GraphSummary(is_empty=False)

        # Classes
        match = self.get_all("Class")
        summary.classes = match.count()

        # Functions
        match = self.get_all("Function")
        summary.functions = match.count()

        return GraphSummary
