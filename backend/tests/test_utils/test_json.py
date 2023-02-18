import unittest
from parameterized import parameterized
from repograph.utils.json import parse_min_max_line_numbers


class TestJSONUtils(unittest.TestCase):
    @parameterized.expand(
        [
            [{"min_max_lineno": {"min_lineno": 0, "max_lineno": 1}}, 0, 1],
            [{"min_max_lineno": {"min_lineno": 0}}, 0, None],
            [{"min_max_lineno": {"max_lineno": 1}}, None, 1],
            [{"minmax_lineno": {"min_lineno": 0, "max_lineno": 1}}, None, None],
            [{}, None, None],
        ]
    )
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
