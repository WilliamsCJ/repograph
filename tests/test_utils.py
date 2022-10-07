import unittest
from parameterized import parameterized
from repograph.utils import *

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