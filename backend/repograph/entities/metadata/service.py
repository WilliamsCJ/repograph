"""
Metadata entity application logic.
"""
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
