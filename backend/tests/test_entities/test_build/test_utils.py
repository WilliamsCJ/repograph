import unittest
from parameterized import parameterized

from repograph.entities.graph.models.nodes import Class
from repograph.entities.build.utils import find_node_object_by_name


class TestJSONUtils(unittest.TestCase):
    @parameterized.expand(
        [
            [
                "TestClient",
                "starlette.testclient.TestClient",
                "fastapi.testclient.TestClient",
            ],
        ]
    )
    def test_find_node_object_by_name(self, name, canonical_name, call):
        """
        Test find_node_object_by_name
        """
        nodes = [
            Class(name=name, canonical_name=canonical_name, repository_name="REPO")
        ]

        result = find_node_object_by_name(nodes, call)
        self.assertIsNotNone(result)
