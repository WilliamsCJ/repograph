"""
Metadata entity application logic.
"""
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

    def register_graph(self, graph: Graph):
        """Register a new graph.

        Args:
            graph (Graph): Graph metadata.

        Returns:
            None
        """
        self.repository.add_database(graph)

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
