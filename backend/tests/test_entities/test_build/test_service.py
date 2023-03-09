import datetime
import os
import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from py2neo import Transaction

from repograph.entities.build.service import BuildService
from repograph.entities.graph.service import GraphService
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.service import MetadataService

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_OUTPUT = "./tmp"


class TestBuildService(unittest.TestCase):

    def setUp(self) -> None:
        self.summarizeMock = MagicMock()
        self.summarizeMock.summarize_function.return_value = "FAKE SUMMARIZATION"
        self.summarizeMock.active = True
        self.txMock = MagicMock(autospec=Transaction)
        self.graphMock = MagicMock(autospec=GraphService)
        self.metadataMock = MagicMock(autospec=MetadataService)
        self.service = BuildService(self.graphMock, self.summarizeMock, self.metadataMock)

    @parameterized.expand([[THIS_DIR + "/../../../../demo/pyLODE"]])
    def test_build_no_errors(self, path: str):
        self.graphMock.get_transaction.return_value = self.txMock
        self.graphMock.get_system_transaction.return_value.__enter__.return_value = (MagicMock(), MagicMock())
        self.graphMock.create_graph.return_value = Graph(name="name", neo4j_name="name", description="description", created=datetime.datetime.now())

        try:
            self.service.build([path], "name", "description", prune=True)
        except Exception:
            self.fail("Test failed with exception")
