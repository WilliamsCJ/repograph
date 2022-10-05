from types.nodes import NodeABC, Repository
from typing import Dict, Any

from repograph.neo4j import Neo4JDatabase
from repograph.repograph import Repograph

ADDITIONAL_KEYS = [
  "requirements",
  "directory_tree",
  "license",
  "readme_files"
]

class RepographBuilder: 
  repograph: Repograph
  
  def __init__(self, uri, user, password, database) -> None:
    self.repograph = Repograph(uri, user, password, database)
    
  def build(self, directory_info: Dict[str, any]) -> Repograph:
    # TODO: Create repository node
    self._create_repository()
    
    # TODO: Parse requirements to create dependency nodes
    self._parse_requirements(directory_info.pop("requirements", None))
    
    # TODO: Parse directory for an unknown reason
    self._parse_directory_tree(directory_info.pop("directory_tree", None))
    
    # TODO: Create license node
    self._parse_license(directory_info.pop("license", None))
    
    # TODO: Create readme nodes
    self._parse_readme(directory_info.pop("readme_files", None))
    
    # Create a sorted list of directory paths, as dictionaries are not always sortable in Python.
    directories = list(directory_info.keys()).sort()

    for directory in directories:
      # TODO: Strip the first part of the path
      # 
    
    # TODO: For directory node in repository create directory
      # TODO: For file node in directory node, create file
    pass
  
  def _create_folder(folder_info, parent):
    
    
  def _create_repository(self, name):
    repository = Repository(name=name)
    self.repograph.create_node(repository)
