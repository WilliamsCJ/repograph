import json
import logging
from pydantic import BaseModel

class NodeABC(BaseModel):  
  def create_cypher_template(self):
    attributes = "{" + ",".join([f"{field}: ${field}" for field in self.__fields_set__]) + "}"
    template = f"CREATE (node:{self.__class__.__name__} {attributes})"
    
    return template
  

class Package(NodeABC):
  name: str
  