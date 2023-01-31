""""
"""
# Base imports
from typing import Tuple

# pip imports
from py2neo import Graph, NodeMatch, Transaction

# Models
from repograph.models.base import BaseSubgraph


class GraphRepository:
    _graph: Graph

    def __init__(self, graph: Graph) -> None:
        """Neo4JDatabase constructor.

        Args:
            graph (Graph): Neo4j database connection.
        """
        print(graph)
        self._graph = graph

    def create_transaction(self) -> Transaction:
        return self._graph.begin()

    def add(self, *args: BaseSubgraph, tx: Transaction = None):
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
        return self._graph.nodes.match().count() != 0

    def get_all(self, label: str) -> Tuple[NodeMatch, int]:
        match: NodeMatch = self._graph.nodes.match(label)
        return match.all(), match.count()
