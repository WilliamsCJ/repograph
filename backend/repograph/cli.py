"""
Command-Line Interface for manual invocation.
"""
import configargparse


from repograph.utils.logging import configure_logging
from repograph.builder.repograph_builder import RepographBuilder
from repograph.utils.json import read_json_from_file

# configure_logging()
#
# DEFAULT_CONFIG = "default.ini"
#
#
# def configure(ctx, _, filename):
#     config = ConfigParser()
#     config.read(filename)
#     print(filename)
#     try:
#         options = dict(**config['general'], **config['neo4j'])
#     except KeyError as e:
#         print(e)
#         options = {}
#     print(options)
#     ctx.default_map = options
#
#
# def validate(**kwargs):
#     required_options = ["username", "password", "database", "input", "prune", "summarize"]
#
#     print(required_options)
#     print(kwargs)
#
#     for option in required_options:
#         if option not in kwargs:
#             raise Exception(f"{option} not specified!")
#
#
# @click.command()
# @click.option(
#   '-c', '--config',
#   type=click.Path(dir_okay=False),
#   callback=configure,
#   is_eager=True,
#   expose_value=False,
#   help="The configuration file",
#   show_default=True
# )
# @click.option(
#   '--uri',
#   type=str,
#   is_flag=False,
#   help="The URI of the Neo4J server.")
# @click.option(
#   '--username',
#   type=str,
#   is_flag=False,
#
#   help="The username to supply to the Neo4J server.")
# @click.option(
#   '--password',
#   type=str,
#   is_flag=False,
#   help="The password to supply to the Neo4J server.")
# @click.option(
#   "--database",
#   type=str,
#   help="The database name to use.")
# @click.option(
#   "-i",
#   "--input",
#   is_flag=False,
#   help="The directory_info.json file."
# )
# @click.option(
#     "--prune",
#     is_flag=True,
#     type=bool,
#     required=True,
#     help="Prune any existing nodes and relationships from the database."
# )
# @click.option(
#     "-s", "--summarize",
#     is_flag=True,
#     type=bool,
#     help="Whether to generate function summarization docstrings"
# )
# def main(*args):
#     validate(**kwargs)
#     builder = RepographBuilder(**kwargs)
#     directory_info = read_json_from_file(kwargs["input"])
#
# def main(uri, username, password, database, input, prune, summarize):
#     builder = RepographBuilder(uri, username, password, database, prune, summarize)
#     directory_info = read_json_from_file(input)
#     repograph = builder.build(directory_info)  # noqa


p = configargparse.ArgParser()
p.add_argument('-c', '--config', is_config_file=True, help='Config file path.')
p.add_argument('--uri', required=True, help='The URI of the Neo4J server.')
p.add_argument('--username', required=True, help='The username to supply to the Neo4J server.')
p.add_argument('--password', required=True, help='The password to supply to the Neo4J server.')
p.add_argument('--database', required=False, default='neo4j', help="The database name to use.")
p.add_argument('--input', required=True, help='The directory_info.json file.')
p.add_argument('--prune', required=False, default=False, help='Prune any existing nodes and relationships from the database.')
p.add_argument('--summarize', required=False, default=False, help='"Whether to generate function summarization docstrings')


if __name__ == "__main__":
    options = p.parse_known_args()
    print(options)
    # main(options)
