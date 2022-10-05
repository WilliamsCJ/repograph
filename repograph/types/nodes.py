import ast
import json
import logging
from pydantic import BaseModel

class NodeABC(BaseModel):  
  def create_cypher_template(self):
    attributes = "{" + ",".join([f"{field}: ${field}" for field in self.__fields_set__]) + "}"
    template = f"CREATE (node:{self.__class__.__name__} {attributes})"
    
    return template
  

class Repository(NodeABC):
  type: str


class Folder(NodeABC):
  name: str
  path: str
  

class File(NodeABC):
  name: str
  path: str
  
  
class Class(NodeABC):
  name: str
  
  
class Function(NodeABC):
  name: str
  source_code: str
  ast: ast.AST
  