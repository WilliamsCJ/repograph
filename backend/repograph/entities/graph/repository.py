"""
Graph database repository.
"""
# Base imports
from typing import Any, Dict, List, Tuple
from logging import getLogger

# pip imports
from py2neo import Graph, NodeMatch, Transaction, Node as py2neoNode

# Models
from repograph.models.base import BaseSubgraph, Node

# Util imports
from repograph.utils.neo4j import create_indices

# Configure logging
log = getLogger('repograph.entities.graph.repository')


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
        self._graph = graph

        # Create indices
        create_indices(self._graph)

    def get_transaction(self) -> Transaction:
        return self._graph.begin()

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

    def get_number_of_nodes_and_relationships(self) -> Tuple[int, int]:
        """Retrieve the number of nodes and relationships in the graph.

        Return:
            int: Number of nodes
            int: Number of relationships
        """
        return self._graph.nodes.match().count(), self._graph.relationships.match().count()

    def get_all_nodes_by_label(self, node_label: type[Node]) -> List[Node]:
        """Retrieve all nodes with a particular label.

        Args:
            node_label(type[Node]): The Node type to fetch. Used to map to label.

        Return:
            List[Node]
        """
        match: NodeMatch = self._graph.nodes.match(node_label.__name__)

        def cast(node: py2neoNode):
            properties = dict(node)
            if "id" in properties:
                properties.pop("id")

            new = node_label(identity=node.identity, **properties)
            new._subgraph.identity = node.identity
            return new

        return list(map(cast, match.all()))

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a Cypher query.

        Args:
            query (str): The Cypher query.

        Return:
            List[Dict[str, Any]]
        """
        cursor = self._graph.query(query)
        return cursor.data()

    def delete_all(self) -> None:
        """Deletes all nodes from the graph.

        Returns:
            None
        """
        self._graph.delete_all()
