"""
Graph database repository.
"""
# Base imports
from typing import Any, Dict, List, Tuple
from logging import getLogger

# pip imports
from py2neo import GraphService, NodeMatch, Transaction, Node as py2neoNode

# Models
from repograph.models.base import BaseSubgraph, Node

# Configure logging
log = getLogger('repograph.entities.graph.repository')


class GraphRepository:
    """
    Neo4j repository. Provides specific interface for Neo4j, using py2neo.
    """
    _graph_service: GraphService

    def __init__(self, graph: GraphService) -> None:
        """Neo4JDatabase constructor.

        Args:
            graph (Graph): Neo4j database connection.
        """
        self._graph_service = graph

    def get_transaction(self, graph_name) -> Transaction:
        """Begin transaction for named graph

        Args:
            graph_name (str): The name of the graph
        """
        if not graph_name:
            raise ValueError("No graph name provided")

        return self._graph_service[graph_name].begin()

    def add(self, *args: BaseSubgraph, graph_name: str = None, tx: Transaction = None) -> None:
        """Add nodes/relationships to the graph.

        Args:
            *args (BaseSubgraph): The nodes and/or relationships to add.
            graph_name (str): The graph name to execute query on.
            tx (Transaction): Optional, existing Transaction to use.

        Return:
            None
        """
        args = list(filter(lambda item: item is not None, args))

        if not tx:
            transaction = self._graph_service[graph_name].begin()
        else:
            transaction = tx

        for arg in args:
            transaction.create(arg._subgraph)

        if not tx:
            transaction.commit()

    def has_nodes(self, graph_name: str = None) -> bool:
        """Checks whether the graph contains any nodes.

        Args:
            graph_name (str): The name of the graph

        Return:
            bool
        """
        return self._graph_service[graph_name].nodes.match().count() != 0

    def get_number_of_nodes_and_relationships(self, graph_name: str = None) -> Tuple[int, int]:
        """Retrieve the number of nodes and relationships in the graph.

        Args:
            graph_name (str): The graph name to execute query on.

        Return:
            int: Number of nodes
            int: Number of relationships
        """
        return \
            self._graph_service[graph_name].nodes.match().count(), \
            self._graph_service[graph_name].relationships.match().count()

    def get_all_nodes_by_label(self, node_label: type[Node], graph_name: str = None) -> List[Node]:
        """Retrieve all nodes with a particular label.

        Args:
            node_label(type[Node]): The Node type to fetch. Used to map to label.
            graph_name (str): The graph name to execute query on.

        Return:
            List[Node]
        """
        match: NodeMatch = self._graph_service[graph_name].nodes.match(node_label.__name__)

        def cast(node: py2neoNode):
            properties = dict(node)
            if "id" in properties:
                properties.pop("id")

            new = node_label(identity=node.identity, **properties)
            new._subgraph.identity = node.identity
            return new

        return list(map(cast, match.all()))

    def execute_query(self, query: str, graph_name: str = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query.

        Args:
            query (str): The Cypher query.
            graph_name (str): The graph name to execute query on.

        Return:
            List[Dict[str, Any]]
        """

        cursor = self._graph_service[graph_name].query(query)
        return cursor.data()

    def delete_all(self, graph_name: str = None) -> None:
        """Deletes all nodes from the graph.

        Args:
            graph_name (str): Graph name to execute query on.

        Returns:
            None
        """
        self._graph_service[graph_name].delete_all()
