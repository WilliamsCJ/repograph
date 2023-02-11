import sqlite3
import unittest
import datetime
from unittest.mock import MagicMock

from repograph.entities.metadata.repository import MetadataRepository
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.utils import datetime_to_string


class TestGraphRepository(unittest.TestCase):
    repository: MetadataRepository

    def setUp(self):
        self.db = MagicMock(autospec=sqlite3.Connection)
        self.repository = MetadataRepository(self.db)

    def test_list_databases(self):
        self.repository.list_databases()
        self.db.execute.assert_called_with("SELECT * FROM graphs")

    def test_add_database(self):
        graph = Graph(
            neo4j_name="test",
            name="test",
            description="description",
            created=datetime.datetime.now()
        )

        self.repository.add_database(graph)
        self.db.execute.assert_called_with(
            "INSERT INTO graphs VALUES (?, ?, ?, ?)",
            (graph.neo4j_name, graph.name, graph.description, datetime_to_string(graph.created))
        )
