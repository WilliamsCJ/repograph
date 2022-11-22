"""
Main module.
"""

import click

from repograph.logging import configure_logging
from repograph.repograph_builder import RepographBuilder
from repograph.utils import read_json_from_file

configure_logging()


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
@click.option(
    "-s", "--summarize",
    is_flag=True,
    type=bool,
    help="Generate code summarizations."
)
def main(uri, username, password, database, input, prune, summarize):
    print(summarize)
    builder = RepographBuilder(uri, username, password, database, prune, summarize)
    directory_info = read_json_from_file(input)
    repograph = builder.build(directory_info)  # noqa


if __name__ == "__main__":
    main()
