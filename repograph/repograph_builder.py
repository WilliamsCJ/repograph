from types.nodes import NodeABC, Repository
from typing import Dict, Any

from repograph.neo4j import Neo4JDatabase
from repograph.repograph import Repograph
from repograph.types.nodes import Folder, File
import repograph.utils as utils

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
      self._parse_directory(directory, directory_info[directory])
    
      
  def _parse_directory(self, directory_name, directory_info):
    stripped_path = utils.strip_file_path_prefix(directory_name)
    folder = Folder(stripped_path)
    self.repograph.add_node(folder)
    
    for file in directory_info.values():
      file = File(file["file"]["fileNameBase"], file["file"]["path"], file["file"]["extension"])
      self.repograph.add_node(file)
      self.repograph.add_relationship(folder, file)

    
  def _create_repository(self, name):
    repository = Repository(name=name)
    self.repograph.create_node(repository)

