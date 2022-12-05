import unittest
from parameterized import parameterized
from repograph.utils.paths import strip_file_path_prefix, get_path_name, get_path_parent, \
    is_root_folder, get_path_root


class TestPathUtils(unittest.TestCase):
    @parameterized.expand([
      ["a/b/c", "b/c"],
      ["b/c", "c"],
      ["c/", "."]
    ])
    def test_strip_file_path_prefix(self, original, result):
        self.assertEqual(strip_file_path_prefix(original), result)

    @parameterized.expand([
      ["a/b/c", "c"],
      ["b/c", "c"],
      ["c/", "c"]
    ])
    def test_get_path_name(self, original, result):
        self.assertEqual(get_path_name(original), result)

    @parameterized.expand([
      ["a/b/c", "a/b"],
      ["b/c", "b"],
      ["c/", "."]
    ])
    def test_get_path_parent(self, original, result):
        self.assertEqual(get_path_parent(original), result)

    @parameterized.expand([
      ["a/b/c", False],
      ["b/c", False],
      ["b", True],
      ["c/", True]
    ])
    def test_is_root_folder(self, path, result):
        self.assertEqual(is_root_folder(path), result)

    @parameterized.expand([
      ["a/b/c", "a"],
      ["b/c", "b"],
      ["b", "b"],
      ["c/", "c"]
    ])
    def test_get_path_root(self, path, result):
        self.assertEqual(get_path_root(path), result)
