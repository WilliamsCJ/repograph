"""
Command-Line Interface for manual invocation.
"""
import configargparse
import logging
import os
import subprocess
from typing import Any, Tuple

from repograph.entities.build.builder import RepographBuilder
from repograph.builder.code_analyser import call_inspect4py, cleanup_inspect4py_output
from repograph.utils.exceptions import RepographBuildError
from repograph.utils.json import read_json_from_file
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


if __name__ == "__main__":
    args, _ = p.parse_known_args()
    builder = RepographBuilder(
        args.uri,
        args.username,
        args.password,
        args.database,
        prune=args.prune,
        summarize=args.summarize,
    )

    temp_output = f"./tmp/{args.name}"

    try:
        if args.skip_inspect4py:
            directory_info, call_graph = parse_inspect4py_output(args.input)
        else:
            call_inspect4py(args.input, temp_output)
            directory_info, call_graph = parse_inspect4py_output(temp_output)

        repograph = builder.build(directory_info, call_graph)  # noqa
    except subprocess.CalledProcessError as e:
        log.error("Error invoking inspect4py - %s", str(e))
    except RepographBuildError as e:
        log.error("Error building repograph - %s", str(e))
    finally:
        if not args.skip_inspect4py:
            cleanup_inspect4py_output()
