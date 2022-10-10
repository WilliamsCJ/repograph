import unittest
from parameterized import parameterized
from repograph.models.nodes import Folder


class TestFolder(unittest.TestCase):

    @parameterized.expand([
      ["a/b/c", "c", "a/b"]
    ])
    def test_attributes(self, path, name, parent):
        package = Folder(path)
        self.assertEqual(package.name, name)
        self.assertEqual(package.parent, parent)
        self.assertEqual(package.path, path)
