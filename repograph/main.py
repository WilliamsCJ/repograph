import click
from repograph import Repograph
from repograph.utils import read_json_from_file

@click.command()
@click.option(
  '--uri', 
  type=str, 
  is_flag=False, 
  help="The URI of the Neo4J server.")
@click.option(
  '--username', 
  type=str, 
  is_flag=False, 
  help="The username to supply to the Neo4J server.")
@click.option(
  '--password', 
  type=str, 
  is_flag=False, 
  help="The password to supply to the Neo4J server.")
@click.option(
  "--database",
  type=str,
  help="The database name to use.")
@click.option(
  "-i",
  "--input",
  is_flag=False,
  help="The directory_info.json file."
)
def main(uri, username, password, database):
  database = Ne
  builder = RepographBuilder(username, password, database)
  
  repograph = Repograph(uri, username, password, database)
  

if __name__ == "__main__":
  main()
