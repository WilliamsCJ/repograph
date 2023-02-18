"""
Metadata repository.
"""
# Base imports
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
        self.db_path = "./test.db"  # TODO: Change back.
        db = sqlite3.connect(self.db_path)
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS graphs
            (neo4j_name TEXT, name TEXT, description TEXT, created TEXT, status TEXT, PRIMARY KEY(neo4j_name));
        """
        )

    def get_transaction(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.db_path)
        return db

    def list_databases(self) -> List[Graph]:
        """List the metadata for all databases.

        Returns:
            List[Graph]
        """
        db = sqlite3.connect(self.db_path)
        rows = db.execute("SELECT * FROM graphs")
        return list(
            map(
                lambda row: Graph(
                    neo4j_name=row[0],
                    name=row[1],
                    description=row[2],
                    created=string_to_datetime(row[3]),
                    status=row[4],
                ),
                rows.fetchall(),
            )
        )

    @classmethod
    def add_database(cls, graph: Graph, db: sqlite3.Connection) -> None:
        """Add a Graph to the metadata database.

        Args:
            graph (Graph): Graph metadata.
            db (sqlite3.Connection): Transaction

        Returns:
            None
        """
        db.execute(
            "INSERT INTO graphs VALUES (?, ?, ?, ?, ?)",
            (
                graph.neo4j_name,
                graph.name,
                graph.description,
                datetime_to_string(graph.created),
                graph.status,
            ),
        )

    def delete_database(self, name: str) -> None:
        """Delete graph metadata

        Args:
            name (str): Neo4j name of the graph.

        Returns:
            None
        """
        db = sqlite3.connect(self.db_path)
        db.execute(f"DELETE FROM graphs WHERE neo4j_name = '{name}'")
        db.commit()

    def update_database(self, graph: Graph) -> None:
        """Update the details of a graph.

        Args:
            graph (Graph): Updated Graph object.

        Returns:
            None
        """
        db = sqlite3.connect(self.db_path)
        db.execute(
            "UPDATE graphs SET name = ?, description = ?, status = ? WHERE neo4j_name = ?",
            (graph.name, graph.description, graph.status, graph.neo4j_name),
        )
        db.commit()
