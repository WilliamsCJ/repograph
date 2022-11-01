import unittest
from parameterized import parameterized
from repograph.models.nodes import Class, File, Folder


class TestFolder(unittest.TestCase):

    @parameterized.expand([
      ["a/b/c", "c", "a/b"]
    ])
    def test_attributes(self, path, name, parent):
        package = Folder(path)
        self.assertEqual(package.name, name)
        self.assertEqual(package.parent, parent)
        self.assertEqual(package.path, path)


class TestFile(unittest.TestCase):

    @parameterized.expand([
      ["file.py", "/dir/file.py", ".py", False]
    ])
    def test_attributes(self, name, path, extension, is_test):
        file = File(name, path, extension, is_test)
        self.assertEqual(file.name, name)
        self.assertEqual(file.path, path)
        self.assertEqual(file.extension, extension)
        self.assertEqual(file.is_test, is_test)


class TestClass(unittest.TestCase):

    @parameterized.expand([
      ["Class", 1, 2, ["SuperClass"]]
    ])
    def test_attributes(self, name, min_line, max_line, extends):
        classNode = Class(name, min_line, max_line, extends)
        self.assertEqual(classNode.name, name)
        self.assertEqual(classNode.min_line_number, min_line)
        self.assertEqual(classNode.max_line_number, max_line)
        self.assertEqual(classNode.extends, extends)
