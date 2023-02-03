"""
Graph entity application logic.
"""
# Base imports
from logging import getLogger
from typing import Dict, List

# Model imports
from repograph.models.base import Node, Relationship
from repograph.models.nodes import Class, Function, Module, Repository
from repograph.models.graph import GraphSummary

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository

# Configure logging
log = getLogger('repograph.entities.graph.service')


class GraphService:
    """
    The GraphService class implements all application-logic related to the graph entity.
    """
    repository: GraphRepository

    def __init__(self, repository: GraphRepository):
        """Constructor

        Args:
            repository (GraphRepository): The Neo4j graph repository.
        """
        self.repository = repository

    def bulk_add(self, nodes: List[Node], relationships: List[Relationship]):
        """Bulk add nodes and relationships.

        Args:
            nodes (List[Node]): Nodes to add.
            relationships (List[Relationship]): Relationships to add.

        Return:
            None
        """
        self.repository.add(*nodes, *relationships)

    def get_summary(self) -> GraphSummary:
        """Calculate a summary of the graph.

        Return:
            GraphSummary
        """
        if not self.repository.has_nodes():
            log.warning("Graph has no nodes")
            return GraphSummary()

        summary = GraphSummary(is_empty=False)

        # Nodes and relationships totals
        nodes, relationships = self.repository.get_number_of_nodes_and_relationships()
        summary.nodes_total = nodes
        summary.relationships_total = relationships

        # Repositories
        _, count = self.repository.get_all_nodes_by_label(Repository)
        summary.repositories = count

        # Modules
        _, count = self.repository.get_all_nodes_by_label(Module)
        summary.modules = count

        # Classes
        _, count = self.repository.get_all_nodes_by_label(Class)
        summary.classes = count

        # Functions
        _, count = self.repository.get_all_nodes_by_label(Function)
        summary.functions = count

        return summary

    def get_function_summarizations(self) -> Dict[str, Function]:
        """Converts all Function nodes into a list of tuples.

        Tuple: (summarization, node)

        Returns:
            List[Tuple[str, Function]
        """
        nodes = self.repository.execute_query(
            """
            MATCH (n:Docstring)-[:Documents]-(f:Function) WHERE n.summarization IS NOT NULL
            RETURN n.summarization as `summarization`, f as `function`
            """
        )
        return dict(map(lambda x: (x['summarization'], x['function']), nodes))

    def prune(self):
        """Delete all nodes and relationships from the graph."""
        self.repository.delete_all()
