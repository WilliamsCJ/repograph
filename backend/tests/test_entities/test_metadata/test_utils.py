import datetime
import unittest
from parameterized import parameterized
from repograph.entities.metadata.utils import datetime_to_string, string_to_datetime


class TestMetadataUtils(unittest.TestCase):
    @parameterized.expand([
        [datetime.datetime(2022, 2, 23, 9, 25, 0), "2022-02-23 09:25:00.000"],
    ])
    def test_datetime_to_string(self, original, target):
        output = datetime_to_string(original)
        self.assertEqual(output, target)

    @parameterized.expand([
        ["2022-02-23 09:25:00.000", datetime.datetime(2022, 2, 23, 9, 25, 0)],
    ])
    def test_string_to_datetime(self, original, target):
        output = string_to_datetime(original)
        self.assertEqual(output, target)
