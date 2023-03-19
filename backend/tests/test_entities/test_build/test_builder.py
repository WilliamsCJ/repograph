import os
import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from py2neo import Transaction

from repograph.entities.build.builder import RepographBuilder
from repograph.entities.build.service import BuildService
from repograph.entities.graph.service import GraphService

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_OUTPUT = "./tmp"


class TestRepographBuilderIntegration(unittest.TestCase):
    builder: RepographBuilder

    def setUp(self) -> None:
        self.summarizeMock = MagicMock()
        self.summarizeMock.return_value = "FAKE SUMMARIZATION"
        self.txMock = MagicMock(autospec=Transaction)
        self.graphMock = MagicMock(autospec=GraphService)
        self.builder = RepographBuilder(
            self.summarizeMock, TEMP_OUTPUT, "TEST", self.graphMock, self.txMock
        )

    @parameterized.expand([
        [THIS_DIR + "/../../../../demo/pyLODE"],
        [THIS_DIR + "/../../../../demo/black"],
        [THIS_DIR + "/../../../../demo/fastapi"],
        [THIS_DIR + "/../../../../demo/flake8"],
        [THIS_DIR + "/../../../../demo/pygorithm"],
        [THIS_DIR + "/../../../../demo/starlette"],
        [THIS_DIR + "/../../../../demo/missing_dependency"],
        [THIS_DIR + "/../../../../demo/circular_dependency"]

    ])
    def test_build_no_errors(self, path: str):
        try:
            BuildService.call_inspect4py(path, TEMP_OUTPUT)
            directory_info, call_graph = BuildService.parse_inspect4py_output(
                TEMP_OUTPUT
            )

            self.builder.build(directory_info, call_graph)
        except Exception:
            self.fail("Test failed with exception")
