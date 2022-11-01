"""
Neo4J Graph Database related functionality.
"""
from typing import Optional, Union

from py2neo import Graph

from repograph.models import NodeABC, RelationshipABC


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

    def add(self, *args: Union[NodeABC, RelationshipABC]):
        """Adds a node to the Neo4J graph.

        Args:
            *args: Nodes or relationships to add.

        Returns:
            None
        """
        if len(args) == 1:
            self.graph.create(*args)
        else:
            tx = self.graph.begin()
            for arg in args:
                tx.create(arg)
            tx.commit()

    def find(self, node_type: str, name: str) -> Optional[NodeABC]:
        """

        Args:
            node_type:
            name:

        Returns:

        """
        result = self.graph.nodes.match(name=name)
        return result.first()
