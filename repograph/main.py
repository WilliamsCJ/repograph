import click
from repograph import Repograph

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
  help="The database name to use")
def main(uri, username, password, database):
  repograph = Repograph(uri, username, password, database)
  print("Connected")
  repograph.createModule()

if __name__ == "__main__":
  main()
