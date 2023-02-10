import unittest
from unittest.mock import MagicMock

from py2neo import GraphService, Graph

from repograph.models.nodes import Function
from repograph.entities.graph.repository import GraphRepository


GRAPH_NAME = "example"


class TestGraphRepository(unittest.TestCase):
    repository: GraphRepository

    def setUp(self):
        self.neo4j = MagicMock(autospec=GraphService)
        self.graph = MagicMock(autospec=Graph)
        self.neo4j.__getitem__.return_value = self.graph
        self.repository = GraphRepository(self.neo4j)

    def test_begin_transaction(self):
        self.repository.get_transaction(GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.begin.assert_called()

    def test_has_nodes(self):
        self.repository.has_nodes(graph_name=GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.nodes.match.assert_called()

    def test_get_number_of_nodes_and_relationships(self):
        self.repository.get_number_of_nodes_and_relationships(graph_name=GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.nodes.match.assert_called()

    def test_get_all_nodes_by_label(self):
        label = Function
        self.repository.get_all_nodes_by_label(label, graph_name=GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.nodes.match.assert_called_with(label.__name__)

    def test_execute_query(self):
        query = 'query'
        self.repository.execute_query(query, graph_name=GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.query.assert_called_with(query)

    def test_delete_all(self):
        self.repository.delete_all(graph_name=GRAPH_NAME)
        self.neo4j.__getitem__.assert_called_with(GRAPH_NAME)
        self.graph.delete_all.assert_called_with()
