import abc
import ast
from py2neo import Node

import repograph.utils as utils

class NodeABC(abc.ABC, Node):
  def __init__(self, **kwargs) -> None:
    super().__init__(self.__class__.__name, **kwargs)
    

class Folder(NodeABC):
  name: str
  path: str
  parent: str
  
  def __init__(self, path):
    self.path = path
    self.name = utils.get_path_name(path)
    self.parent = utils.get_path_parent(path)
    super().__init__( path=self.path, name=self.name, parent=self.parent)
  

class Repository(NodeABC):
  type: str
  
  def __init__(self, type) -> None:
    self.type = type
    super().__init__(type=type)
  

class File(NodeABC):
  name: str
  path: str
  extension: str
  
  def __init__(self, name, path, extension) -> None:
    self.path = path
    self.name = name
    self.extension = extension
    super().__init__(type=self.type, name=self.name)
  
  
class Class(NodeABC):
  name: str
  
  
class Function(NodeABC):
  name: str
  source_code: str
  ast: ast.AST

class Body(NodeABC):
  pass