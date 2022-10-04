from neo4j import GraphDatabase

class Repograph:
  database: str 
  
  def __init__(self, uri, user, password, database) -> None:
    self.driver = GraphDatabase.driver(uri, auth=(user, password))
    self.database = database
    
  def create_package(self):
    pass
    # print(self.database)
    # with self.driver.session(database=self.database) as session:
    #   module = session.execute_write(self._create_and_return_module, "test_module")
    #   print(module)
    
  def create_module(self):
    pass
  
  def create_class(self):
    pass
  
  def create_method():
    pass
  
  def create_function():
  
  
      
  @staticmethod
  def _create_and_return_module(tx, name):
      query = (
        "CREATE (test:Module { name: $name })"
        "RETURN test"
      )
      
      result = tx.run(
        query,
        name=name
      )
    
      return result.single()[0]