"""
Main module.
"""
from configparser import ConfigParser
import click

from repograph.logging import configure_logging
from repograph.repograph_builder import RepographBuilder
from repograph.utils import read_json_from_file

configure_logging()

DEFAULT_CONFIG = "default.ini"


def configure(ctx, _, filename):
    config = ConfigParser()
    config.read(filename)
    print(filename)
    try:
        options = dict(**config['general'], **config['neo4j'])
    except KeyError as e:
        print(e)
        options = {}
    print(options)
    ctx.default_map = options


def validate(**kwargs):
    required_options = ["username", "password", "database", "input", "prune", "summarize"]

    print(required_options)
    print(kwargs)

    for option in required_options:
        if option not in kwargs:
            raise Exception(f"{option} not specified!")


@click.command()
@click.option(
  '-c', '--config',
  type=click.Path(dir_okay=False),
  callback=configure,
  is_eager=True,
  expose_value=False,
  help="The configuration file",
  show_default=True
)
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
    required=True,
    help="Prune any existing nodes and relationships from the database."
)
@click.option(
    "--summarize",
    is_flag=True,
    type=bool,
    help="Whether to generate function summarization docstrings"
)
def main(**kwargs):
    validate(**kwargs)
    builder = RepographBuilder(**kwargs)
    directory_info = read_json_from_file(kwargs["input"])
    repograph = builder.build(directory_info)  # noqa


if __name__ == "__main__":
    main()
