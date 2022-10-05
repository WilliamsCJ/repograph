"""
Neo4J Graph Database related functionality.
"""

from neo4j import GraphDatabase, Driver

from repograph.types import NodeABC

class Neo4JDatabase:
  """A connected Neo4J database.
  
  Represents a connection to a Neo4J graph database, 
  and provides functionality for interacting with it.
  """
  driver: Driver
  database: str
  
  def __init__(self, uri, user, password, database) -> None:
    """Neo4JDatabase constructor.

    Args:
        uri (_type_): _description_
        user (_type_): _description_
        password (_type_): _description_
        database (_type_): _description_
    """
    self.driver = GraphDatabase.driver(uri, auth=(user, password))
    self.database = database
    
  def create_node(self, node: NodeABC) -> NodeABC:
    """Creates a node in the database.

    Args:
        node (NodeABC): The Node to create in the database.

    Returns:
        NodeABC: The created node.
    """
    # TODO: Do we want to return this? Given that it is an argument also?
    with self.driver.session(database=self.database) as session:
      def transaction_func(tx, node: NodeABC):
        query = node.create_cypher_template()
        result = tx.run(query, node.dict())
        record = result.single()
        return record[0]
      
      result = session.execute_write(transaction_func, node)
      return result