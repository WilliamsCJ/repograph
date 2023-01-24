"""
Neo4J Graph Database related functionality.
"""
import logging
from py2neo import Graph, NodeMatch
from typing import Tuple

from repograph.models.base import BaseSubgraph

log = logging.getLogger('repograph.utils.neo4j')


class Neo4JDatabase:
    """A connected Neo4J database.

    Represents a connection to a Neo4J graph database,
    and provides functionality for interacting with it.
    """
    graph: Graph
    database: str

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j") -> None:
        """Neo4JDatabase constructor.

        Args:
            uri (_type_): _description_
            user (_type_): _description_
            password (_type_): _description_
            database (_type_): _description_
        """
        self.graph = Graph(uri, auth=(user, password), name=database)
        self.database = database

    def add(self, *args: BaseSubgraph):
        args = list(filter(lambda item: item is not None, args))
        tx = self.graph.begin()
        for arg in args:
            tx.create(arg._subgraph)
        tx.commit()

    def has_nodes(self) -> bool:
        return self.graph.nodes.match().count() != 0

    def get_all(self, label: str) -> Tuple[NodeMatch, int]:
        match: NodeMatch = self.graph.nodes.match(label)
        return match.all(), match.count()
