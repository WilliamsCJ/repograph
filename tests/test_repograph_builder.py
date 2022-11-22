import os
import unittest
from unittest.mock import MagicMock

from repograph.repograph_builder import RepographBuilder
from repograph.utils import read_json_from_file


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestableRepographBuilder(RepographBuilder):
    summarize: bool = False

    def __init__(self, uri, user, password, database, prune=False, summarize=False) -> None:
        self.repograph = MagicMock()
        self.function_summarizer = MagicMock()


class TestRepographBuilderIntegration(unittest.TestCase):
    def test_build_no_errors(self):
        try:
            builder = TestableRepographBuilder(
                "uri",
                "user",
                "password",
                "database",
                True,
                False
            )
            directory_info = read_json_from_file(
                os.path.join(
                    THIS_DIR,
                    "data/directory_info.json"
                )
            )
            _ = builder.build(directory_info)
        except Exception:
            self.fail("Test failed with exception")
