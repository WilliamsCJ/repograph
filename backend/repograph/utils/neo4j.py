"""
Neo4J Graph Database related functionality.
"""
from py2neo import Graph, NodeMatch

from repograph.models.base import BaseSubgraph


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
        tx = self.graph.begin()
        for arg in args:
            tx.create(arg._subgraph)
        tx.commit()

    def has_nodes(self) -> bool:
        return self.graph.nodes.match("*").count() != 0

    def get_all(self, label: str) -> NodeMatch:
        return self.graph.nodes.match(label).all()
