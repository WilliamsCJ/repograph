""""
Graph database repository.
"""
# Base imports
from typing import List

# pip imports
from py2neo import Graph, NodeMatch, Transaction, Node as py2neoNode

# Models
from repograph.models.base import BaseSubgraph, Node


class GraphRepository:
    """
    Neo4j repository. Provides specific interface for Neo4j, using py2neo.
    """
    _graph: Graph

    def __init__(self, graph: Graph) -> None:
        """Neo4JDatabase constructor.

        Args:
            graph (Graph): Neo4j database connection.
        """
        print(graph)
        self._graph = graph

    def add(self, *args: BaseSubgraph, tx: Transaction = None) -> None:
        """Add nodes/relationships to the graph.

        Args:
            *args (BaseSubgraph): The nodes and/or relationships to add.
            tx (Transaction): Optional, existing Transaction to use.

        Return:
            None
        """
        args = list(filter(lambda item: item is not None, args))

        if not tx:
            transaction = self._graph.begin()
        else:
            transaction = tx

        for arg in args:
            transaction.create(arg._subgraph)

        if not tx:
            transaction.commit()

    def has_nodes(self) -> bool:
        """Checks whether the graph contains any nodes.

        Return:
            bool
        """
        return self._graph.nodes.match().count() != 0

    def get_all_nodes_by_label(self, node_label: type[Node]) -> List[Node]:
        """Retrieve all nodes with a particular label.

        Args:
            node_label(type[Node]): The Node type to fetch. Used to map to label.

        Return:
            List[Node]
        """
        match: NodeMatch = self._graph.nodes.match(node_label.__name__)

        def cast(node: py2neoNode):
            new = node_label(**dict(node))
            new._subgraph.identity = node.identity
            return new

        return list(map(cast, match.all()))

    def delete_all(self) -> None:
        """Deletes all nodes from the graph.

        Returns:
            None
        """
        self._graph.delete_all()
