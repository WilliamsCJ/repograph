"""
Command-Line Interface for manual invocation.
"""
import configargparse


from repograph.utils.logging import configure_logging
from repograph.builder.repograph_builder import RepographBuilder
from repograph.utils.json import read_json_from_file

configure_logging()

p = configargparse.ArgParser()
p.add_argument('-c', '--config', is_config_file=True, help='Config file path.')
p.add_argument('--uri', required=True, help='The URI of the Neo4J server.')
p.add_argument('--username', required=True, help='The username to supply to the Neo4J server.')
p.add_argument('--password', required=True, help='The password to supply to the Neo4J server.')
p.add_argument('--database', required=False, default='neo4j', help="The database name to use.")
p.add_argument('--input', required=True, help='The directory_info.json file.')
p.add_argument(
    '--prune',
    required=False,
    action="store_true",
    help='Prune any existing nodes and relationships from the database.'
)
p.add_argument(
    '--summarize',
    required=False,
    action="store_true",
    help='"Whether to generate function summarization docstrings'
)


if __name__ == "__main__":
    args, _ = p.parse_known_args()
    builder = RepographBuilder(
        args.uri,
        args.username,
        args.password,
        args.database,
        args.prune,
        args.summarize
    )
    directory_info = read_json_from_file(args.input)
    repograph = builder.build(directory_info)  # noqa
