"""
Metadata repository.
"""
import sqlite3
from typing import List

# Metadata entity imports
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.utils import datetime_to_string, string_to_datetime


class MetadataRepository:
    """
    SQLite3 Repository for storing Graph metadata.

    NOTE: We create a new SQLite3 connection for each method,
    as SQLite connections must be called from the same thread
    they were created in.
    """
    db_path: str

    def __init__(self, db_path: str):
        """
        Constructor
        """
        self.db_path = db_path
        db = sqlite3.connect(db_path)
        db.execute("""
            CREATE TABLE IF NOT EXISTS graphs
            (neo4j_name TEXT, name TEXT, description TEXT, created TEXT, status TEXT)
        """)

    def list_databases(self) -> List[Graph]:
        """List the metadata for all databases.

        Returns:
            List[Graph]
        """
        db = sqlite3.connect(self.db_path)
        rows = db.execute("SELECT * FROM graphs")
        return list(map(lambda row: Graph(
            neo4j_name=row[0],
            name=row[1],
            description=row[2],
            created=string_to_datetime(row[3]),
            status=row[4]
        ), rows.fetchall()))

    def add_database(self, graph: Graph) -> None:
        """Add a Graph to the metadata database.
git psu
        Args:
            graph (Graph): Graph metadata.

        Returns:
            None
        """
        db = sqlite3.connect(self.db_path)
        db.execute(
            "INSERT INTO graphs VALUES (?, ?, ?, ?, ?)",
            (graph.neo4j_name, graph.name, graph.description, datetime_to_string(graph.created), graph.status)  # noqa: 501
        )
        db.commit()

    def update_graph(self, graph: Graph):
        db = sqlite3.connect(self.db_path)
        db.execute(
            "UPDATE graphs SET name = ?, description = ?, status = ? WHERE neo4j_name = ?",
            (graph.name, graph.description, graph.status, graph.neo4j_name)
        )
        db.commit()