import unittest
from parameterized import parameterized
from backend.builder.utils import parse_min_max_line_numbers, strip_file_path_prefix, get_path_name, \
                            get_path_parent, is_root_folder, get_path_root


class TestUtils(unittest.TestCase):
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

    @parameterized.expand([
        [{"min_max_lineno": {"min_lineno": 0, "max_lineno": 1}}, 0, 1],
        [{"min_max_lineno": {"min_lineno": 0}}, 0, None],
        [{"min_max_lineno": {"max_lineno": 1}}, None, 1],
        [{"minmax_lineno": {"min_lineno": 0, "max_lineno": 1}}, None, None],
        [{}, None, None]
    ])
    def test_parse_min_max_line_numbers(self, json, min, max):
        """Test for parse_min_max_line_numbers.

        Should return None for either min or max if information is missing.

        Args:
            json (JSONDict): Test JSON
            min (Optional[int]): Expected min line number
            max (Optional[int]): Expected max line number
        """
        minimum, maximum = parse_min_max_line_numbers(json)
        self.assertEqual(min, minimum)
        self.assertEqual(max, maximum)
