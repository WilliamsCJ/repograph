"""
Command-Line Interface for manual invocation.
"""
# Base imports
import logging
from typing import List

# pip imports
import configargparse
from dependency_injector.wiring import inject, Provide

# Application Container
from repograph.container import ApplicationContainer

# Build service
from repograph.entities.build import BuildService

# Utilities
from repograph.utils.logging import configure_logging

# Configure logging format
configure_logging()
log = logging.getLogger("repograph.cli")

# Command-line / config-file argument parsing
p = configargparse.ArgParser()
p.add_argument('-c', '--config', is_config_file=True, help='Config file path.')
p.add_argument('--uri', required=True, help='The URI of the Neo4J server.')
p.add_argument('--username', required=True, help='The username to supply to the Neo4J server.')
p.add_argument('--password', required=True, help='The password to supply to the Neo4J server.')
p.add_argument('--database', required=False, default='neo4j', help="The database name to use.")
p.add_argument('--input', required=True, help='The directory_info.json file.')
p.add_argument('--name', required=True, help='The name of the repository.')
p.add_argument(
    '--prune',
    required=False,
    action="store_true",
    help='Prune any existing nodes and relationships from the database.'
)
p.add_argument(
    '--summarization',
    required=False,
    action="store_true",
    help='"Whether to generate function summarization docstrings'
)
p.add_argument(
    '--skip_inspect4py',
    required=False,
    action="store_true",
    help='Whether to skip running inspect4py. Use when the input directory '
         'is already an inspect4py output directory.'
)


@inject
def main(
    input_list: List[str],
    build: BuildService = Provide[ApplicationContainer.build.container.service]
) -> None:
    """Main function of CLI script.

    This functionality is broken out into a separate function to provide dependency injection at
    runtime.

    See: https://python-dependency-injector.ets-labs.org/

    Args:
        input_list (List[str]): The list of input paths for the build service.
        build (BuildService): The injected Build Service.

    Returns:
        None
    """
    build.build(input_list)


if __name__ == "__main__":
    args, _ = p.parse_known_args()

    print(type(args))
    print(args)

    # TODO: Pass Neo4j config information
    container = ApplicationContainer()
    container.init_resources()

    main(args.input)


