from pydantic import BaseModel


class LinkABC(BaseModel):  
  def create_cypher_template(self):
    attributes = "{" + ",".join([f"{field}: ${field}" for field in self.__fields_set__]) + "}"
    template = f"CREATE (node:{self.__class__.__name__} {attributes})"
    
    return template
