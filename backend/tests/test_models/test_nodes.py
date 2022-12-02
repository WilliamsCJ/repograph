import unittest

import py2neo
from parameterized import parameterized
from repograph.models.nodes import Class, Docstring, Module, Directory, License


class TestFolder(unittest.TestCase):

    @parameterized.expand([
      ["a/b/c", "c", "a/b"]
    ])
    def test_attributes(self, path, name, parent):
        package = Directory(path)
        self.assertEqual(package.name, name)
        self.assertEqual(package.parent, parent)
        self.assertEqual(package.path, path)


class TestFile(unittest.TestCase):

    @parameterized.expand([
      ["file.py", "/dir/file.py", ".py", False]
    ])
    def test_attributes(self, name, path, extension, is_test):
        file = Module(name=name, path=path, extension=extension, is_test=is_test)
        self.assertEqual(file.name, name)
        self.assertEqual(file.path, path)
        self.assertEqual(file.extension, extension)
        self.assertEqual(file.is_test, is_test)


class TestClass(unittest.TestCase):

    @parameterized.expand([
      ["Class", 1, 2],
      ["Class", None, 2],
      ["Class", 1, None],
      ["Class", None, None]

    ])
    def test_attributes(self, name, min_line, max_line):
        class_node = Class(
            name=name,
            min_line_number=min_line,
            max_line_number=max_line,
        )
        self.assertEqual(class_node.name, name)
        self.assertEqual(class_node.min_line_number, min_line)
        self.assertEqual(class_node.max_line_number, max_line)


class TestLicense(unittest.TestCase):
    @parameterized.expand([
        ["Some text", "MIT", 0.9]
    ])
    def test_attributes(self, text, license_type, confidence):
        license = License(
            text=text,
            license_type=license_type,
            confidence=confidence,
        )
        self.assertEqual(license.text, text)
        self.assertEqual(license.license_type, license_type)
        self.assertEqual(license.confidence, confidence)

    @parameterized.expand([
        ["Some text", "MIT", 0.9]
    ])
    def test_py2neo(self, text, license_type, confidence):
        license = License(
            text=text,
            license_type=license_type,
            confidence=confidence,
        )

        self.assertIsInstance(license._subgraph, py2neo.Node)

        self.assertEqual(license._subgraph.get("text"), text)
        self.assertEqual(license._subgraph.get("license_type"), license_type)
        self.assertEqual(license._subgraph.get("confidence"), confidence)


class TestDocstring(unittest.TestCase):
    @parameterized.expand([
        ["Summarization", "Short Description", "Long description"]
    ])
    def test_attributes(self, summary, short_description, long_description):
        docstring = Docstring(
            short_description=short_description,
            long_description=long_description,
            summarization=summary,
        )
        self.assertEqual(docstring.summarization, summary)

    @parameterized.expand([
        ["Summarization", "Short Description", "Long description"]
    ])
    def test_py2neo(self, summary, short_description, long_description):
        docstring = Docstring(
            short_description=short_description,
            long_description=long_description,
            summarization=summary,
        )

        self.assertIsInstance(docstring._subgraph, py2neo.Node)
        self.assertEqual(docstring._subgraph.get("summarization"), summary)
        self.assertEqual(docstring._subgraph.get("short_description"), short_description)
        self.assertEqual(docstring._subgraph.get("long_description"), long_description)
