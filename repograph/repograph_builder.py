from types.nodes import NodeABC, Repository
from typing import Dict, Any

from repograph.neo4j import Neo4JDatabase
from repograph.repograph import Repograph

class RepographBuilder: 
  repograph: Repograph
  
  def __init__(self, uri, user, password, database) -> None:
    self.repograph = Repograph(uri, user, password, database)
    
  def build(directory_info: Dict[str, any]) -> Repograph:
    # TODO: Create repository node
    self._create_repository()
    
    # TODO: For directory node in repository create directory
      # TODO: For file node in directory node, create file
    pass
    
  def _create_repository(self, name):
    repository = Repository(name=name)
    self.repograph.create_node(repository)
