from unicodedata import name
import unittest
from repograph.types.nodes import Package

class TestPackageNode(unittest.TestCase):
  def test_attributes(self):
    package = Package(name="test")
    assert package.name == "test"
    
  def test_create_cypher_template(self):
    package = Package(name="test")
    template = package.create_cypher_template()
    assert template == "CREATE (node:Package {name: $name})"

