import sqlite3
import unittest
import datetime
from unittest import mock
from unittest.mock import MagicMock

from repograph.entities.metadata.repository import MetadataRepository
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.utils import datetime_to_string


class TestGraphRepository(unittest.TestCase):
    repository: MetadataRepository

    def setUp(self):
        self.repository = MetadataRepository("./test.db")

    def test_list_databases(self):
        with mock.patch("sqlite3.connect") as connectMock:
            connectionMock = MagicMock(auto_spec=sqlite3.Connection)
            connectMock.return_value = connectionMock
            self.repository.list_databases()
            connectionMock.execute.assert_called_with("SELECT * FROM graphs")

    def test_add_database(self):
        graph = Graph(
            neo4j_name="test",
            name="test",
            description="description",
            created=datetime.datetime.now()
        )

        with mock.patch("sqlite3.connect") as connectMock:
            connectionMock = MagicMock(auto_spec=sqlite3.Connection)
            connectMock.return_value = connectionMock
            self.repository.add_database(graph)

            connectionMock.execute.assert_called_with(
                "INSERT INTO graphs VALUES (?, ?, ?, ?)",
                (graph.neo4j_name, graph.name, graph.description, datetime_to_string(graph.created))
            )
