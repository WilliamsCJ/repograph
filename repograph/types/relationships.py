import abc
import ast
from py2neo import Node, Relationship
from repograph.types.nodes import Folder, File, Function, Class, Body

import repograph.utils as utils

class RelationshipABC(abc.ABC, Relationship):
  """Abstract Base Class for Relationships.
  
  Extends the Relationship class from py2neo
  """
  
  def __init__(self, **kwargs) -> "RelationshipABC":
    """RelationshipABC constructor.
    
    Args:
      **kwargs: Keyword arguments
      
    Returns:
      RelationshipABC: An instance of a RelationshipABC subclass.
    """
    super().__init__(self.__class__.__name, **kwargs)
    
    
class InvalidRelationshipException(Exception):
  # TODO: Add error message 
  pass
    
    
class Contains(Relationship):
  """Contains Relationship
  
  Usage:
    - Folder -> Folder/File
    - File -> Class/Function, Body
  """
  
  def __init__(self, parent: Node, child: Node):
    # If parent is a Folder Node, child must be another Folder or a File.
    if (isinstance(parent, Folder) and not(isinstance(child, (Folder, File)))):
      raise InvalidRelationshipException
    
    # If parent is a File Node, child must be a Function, Class or Body node.
    if (isinstance(parent, Folder) and not(isinstance(child, (Function, Class, Body)))):
      raise InvalidRelationshipException
    
    super().__init__(parent, child)