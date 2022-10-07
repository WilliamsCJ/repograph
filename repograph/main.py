import click
from repograph.repograph_builder import RepographBuilder
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
@click.option(
  "--prune",
  is_flag=True,
  type=bool,
  help="Prune any existing nodes and relationships from the database."
)
def main(uri, username, password, database, input, prune):
  builder = RepographBuilder(uri, username, password, database, prune)
  directory_info = read_json_from_file(input)
  repograph = builder.build(directory_info)  

if __name__ == "__main__":
  main()
