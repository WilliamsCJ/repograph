import abc
import ast
from py2neo import Node, Relationship
from typing import Dict, Set

from repograph.models.nodes import Repository, Folder, File, Function, Class, Body, NodeABC
import repograph.utils as utils


class RelationshipABC(abc.ABC, Relationship):
  """Abstract Base Class for Relationships.
  
  Extends the Relationship class from py2neo
  """
  _allowed_types: Dict[Node, Set[Node]]
  
  def __init__(self, parent, child, **kwargs) -> "RelationshipABC":
    """RelationshipABC constructor.
    
    Args:
      **kwargs: Keyword arguments
      
    Returns:
      RelationshipABC: An instance of a RelationshipABC subclass.
    """
    allowed_types = self._allowed_types(type(parent))
    
    if not allowed_types or type(child) not in allowed_types:
      raise InvalidRelationshipException(parent, child, self.__class__.__name)
    
    Relationship.__init__(parent, self.__class__.__name, child, **kwargs)
  
    
class InvalidRelationshipException(TypeError):
  def __init__(self, parent: NodeABC, child: NodeABC, relationship: str) -> None:
    message = f"{type(parent)} -> {type(child)} is not a valid not pairing for relationship of type: {relationship}"
    super().__init__(message)
    
    
class Contains(Relationship):
  """Contains Relationship
  
  Usage:
    - Folder -> Folder/File
    - File -> Class/Function, Body
  """
  _allowed_types = {
    Repository: {Folder, File},
    Folder: {Folder, File},
    File: {Function, Class, Body}
  }
  
  def __init__(self, parent: NodeABC, child: NodeABC):
    # If parent is a Folder Node, child must be another Folder or a File.
    if (isinstance(parent, Folder) and not(isinstance(child, (Folder, File)))):
      raise InvalidRelationshipException()
    
    # If parent is a File Node, child must be a Function, Class or Body node.
    if (isinstance(parent, File) and not(isinstance(child, (Function, Class, Body)))):
      raise InvalidRelationshipException
    
    super().__init__(parent, child)