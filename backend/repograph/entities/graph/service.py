"""

"""
# Base imports
from logging import getLogger
from typing import Dict, List

# Model imports
from repograph.models.base import Node, Relationship
from repograph.models.nodes import Function
from repograph.models.repograph import RepographSummary

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository

# Configure logging
log = getLogger('repograph.entities.graph.service')


class GraphService:
    repository: GraphRepository

    def __init__(self, repository: GraphRepository):
        self.repository = repository

    def bulk_add(self, nodes: List[Node], relationships: List[Relationship]):
        self.repository.add(*nodes, *relationships)

    def get_all_function_nodes(self) -> None:
        self.repository.get_all()

    def get_summary(self) -> RepographSummary:
        if not self.repository.has_nodes():
            log.warning("Graph has no nodes")
            return RepographSummary()

        summary = RepographSummary(is_empty=False)

        # Modules
        _, count = self.repository.get_all("Module")
        summary.modules = count

        # Classes
        _, count = self.repository.get_all("Class")
        summary.classes = count

        # Functions
        _, count = self.repository.get_all("Function")
        summary.functions = count

        return summary

    def get_function_summarizations(self) -> Dict[str, Function]:
        """Converts all Function nodes into a list of tuples.

        Tuple: (summarization, node)

        Returns:
            List[Tuple[str, Function]
        """
        nodes = self.repository.get_all_nodes_by_label(Function)
        print(len(nodes))
        return dict(map(lambda x: (x.summarization, x), nodes))

    def prune(self):
        self.repository.delete_all()
