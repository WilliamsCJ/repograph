import unittest
from parameterized import parameterized

from repograph.entities.graph.models.nodes import Class
from repograph.entities.build.utils import find_node_object_by_name, find_requirements


class TestBuildUtils(unittest.TestCase):
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

    @parameterized.expand(
        [["./tests/test_entities/test_build/test_data", ["package", "another_package"]]]
    )
    def test_find_requirements(self, path, expected_packages):
        """
        Test find_requirements
        """
        result = find_requirements(path)
        assert len(result) == 2
        for req in result:
            assert req.name in expected_packages
        print(result)
