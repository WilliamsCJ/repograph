import unittest
from parameterized import parameterized

from repograph.entities.graph.models.nodes import Class
from repograph.entities.build.utils import find_node_object_by_name, find_requirements, strip_file_path_prefix, is_root_folder, get_path_root, get_module_and_object_from_canonical_object_name


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

    @parameterized.expand([["a/b/c", "b/c"], ["b/c", "c"], ["c/", "."]])
    def test_strip_file_path_prefix(self, original, result):
        self.assertEqual(strip_file_path_prefix(original), result)

    @parameterized.expand([["a/b/c", False], ["b/c", False], ["b", True], ["c/", True]])
    def test_is_root_folder(self, path, result):
        self.assertEqual(is_root_folder(path), result)

    @parameterized.expand([["a/b/c", "a"], ["b/c", "b"], ["b", "b"], ["c/", "c"]])
    def test_get_path_root(self, path, result):
        self.assertEqual(get_path_root(path), result)

    @parameterized.expand([["a.b.c", "a.b", "c"], ["a.b", "a", "b"], ["a", None, "a"]])
    def test_get_module_and_object_from_canonical_object_name(self, path, root, child):
        result_root, result_child = get_module_and_object_from_canonical_object_name(
            path
        )
        self.assertEqual(root, result_root)
        self.assertEqual(child, result_child)
