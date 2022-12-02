"""
This module defines the Repograph class and the operations/queries that can be performed on it
"""
import logging
from typing import List

from repograph.models.repograph import RepographSummary
from repograph.utils.neo4j import Neo4JDatabase

log = logging.getLogger('repograph.repograph')


class Repograph(Neo4JDatabase):
    database: str
    node_types: List[str] = [
        "Class",
        "Function"
    ]

    def __init__(self, uri, user, password, database) -> None:
        super().__init__(uri, user, password, database)

    def get_summary(self) -> RepographSummary:
        if not self.has_nodes():
            log.warning("Graph has no nodes")
            return RepographSummary()

        summary = RepographSummary(is_empty=False)

        # Classes
        _, count = self.get_all("Class")
        summary.classes = count

        # Functions
        _, count = self.get_all("Function")
        summary.functions = count

        return summary
