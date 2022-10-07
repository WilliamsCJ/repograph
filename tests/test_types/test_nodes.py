from unicodedata import name
import unittest
from parameterized import parameterized
from repograph.types.nodes import Folder

class TestFolder(unittest.TestCase):
  
  @parameterized.expand([
    ["name", "path", "parent"]
  ])
  def test_attributes(self, name, path, parent):
    package = Folder(name=name, path=path, parent=parent)
    self.assertEqual(package.name, name)
    self.assertEqual(package.parent, parent)
    self.assertEqual(package.path, path)
    
  @parameterized.expand([
    ["name", "path", "parent"]
  ])
  def test_create_cypher_template(self, name, path, parent):
    package = Folder(name=name, path=path, parent=parent)
    template = package.create_cypher_template()
    self.assertEqual(template, "CREATE (node:Folder {name: $name, parent: $parent, path: $path})")

