import unittest
from parameterized import parameterized
from repograph.entities.graph.utils import get_path_name, get_path_parent


class TestGraphUtils(unittest.TestCase):
    @parameterized.expand([["a/b/c", "c"], ["b/c", "c"], ["c/", "c"]])
    def test_get_path_name(self, original, result):
        self.assertEqual(get_path_name(original), result)

    @parameterized.expand([["a/b/c", "a/b"], ["b/c", "b"], ["c/", "."]])
    def test_get_path_parent(self, original, result):
        self.assertEqual(get_path_parent(original), result)
