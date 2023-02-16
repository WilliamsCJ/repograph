"""
Metadata entity application logic.
"""
import sqlite3

# Base imports
from typing import List

# Metadata entity imports
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.repository import MetadataRepository


class MetadataService:
    repository: MetadataRepository

    def __init__(self, repository: MetadataRepository):
        """Constructor

        Args:
            repository:
        """
        self.repository = repository

    def get_transaction(self) -> sqlite3.Connection:
        return self.repository.get_transaction()

    def register_graph(self, graph: Graph, tx: sqlite3.Connection):
        """Register a new graph.

        Args:
            graph (Graph): Graph metadata.
            tx (sqlite3.Connection): The transaction object.

        Returns:
            None
        """
        self.repository.add_database(graph, tx)

    def get_all_graph_listings(self) -> List[Graph]:
        """Get all graphs

        Returns:
            List[Graph]
        """
        return self.repository.list_databases()

    def set_graph_status_to_created(self, graph: Graph):
        """Set the status of a graph to CREATED.

        Args:
            graph (Graph): Original Graph object to update.

        Returns:
            None
        """
        updated_graph = graph.copy(update={"status": "CREATED"})
        self.repository.update_graph(updated_graph)
