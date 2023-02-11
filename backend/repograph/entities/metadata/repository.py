"""
Metadata repository.
"""
from sqlite3 import Connection
from typing import List

# Metadata entity imports
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.utils import datetime_to_string, string_to_datetime


class MetadataRepository:
    """
    SQLite3 Repository for storing Graph metadata.
    """
    db: Connection

    def __init__(self, db: Connection):
        """
        Constructor
        """
        # self.db = sqlite3.connect(db_path) // TODO: Do in container
        self.db = db
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS graphs
            (neo4j_name TEXT, name TEXT, description TEXT, created TEXT)
        """)

    def list_databases(self) -> List[Graph]:
        """List the metadata for all databases.

        Returns:
            List[Graph]
        """
        rows = self.db.execute("SELECT * FROM graphs")
        return list(map(lambda row: Graph(
            neo4j_name=row[0],
            name=row[1],
            description=row[2],
            created=string_to_datetime(row[3])
        ), rows))

    def add_database(self, graph: Graph) -> None:
        """Add a Graph to the metadata database.

        Args:
            graph (Graph): Graph metadata.

        Returns:
            None
        """
        rows = self.db.execute(
            "INSERT INTO graphs VALUES (?, ?, ?, ?)",
            (graph.neo4j_name, graph.name, graph.description, datetime_to_string(graph.created))
        )
        print(rows)
