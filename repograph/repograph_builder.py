import enum
from neo4j import GraphDatabase

class NodeTypes(enum):
  PACKAGE = "Package"
  MODULE = "Module"
  

class RepographBuilder:
  database: str
  
  def __init__(self, uri, user, password, database) -> None:
    self.driver = GraphDatabase.driver(uri, auth=(user, password))
    self.database = database
    
  def build(directory_info):
    # Create modules
    
  def _create_module():
    
    
  @staticmethod
  def _create_and_return_node(tx, name, ):
      query = (
        "CREATE (node:Module { name: $name })"
        "RETURN node"
      )
      
      result = tx.run(
        query,
        name=name
      )
    
      return result.single()[0]