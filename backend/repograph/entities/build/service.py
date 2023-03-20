"""

"""
# Base imports
import shutil
import subprocess
from logging import getLogger
import os
from typing import Any, List, Tuple

# Build entity imports
from repograph.entities.build.builder import RepographBuilder
from repograph.entities.build.exceptions import RepographBuildError
from repograph.entities.build.utils import read_json_from_file, find_requirements

# Other service imports
from repograph.entities.graph.service import GraphService
from repograph.entities.summarization.service import SummarizationService
from repograph.entities.metadata.service import MetadataService


# Configure logging
log = getLogger("repograph.entities.build.service")


class BuildService:
    graph: GraphService
    summarization: SummarizationService
    metadata: MetadataService

    temp_output = "./tmp"

    def __init__(
        self,
        graph: GraphService,
        summarization: SummarizationService,
        metadata: MetadataService,
        extract_metadata: bool = False
    ):
        """Constructor

        Args:
            graph (GraphService): The Graph Service.
            summarization (SummarizationService): The Summarization Service
            metadata (MetadataService): The Metadata Service
        """
        self.graph = graph
        self.summarization = summarization
        self.metadata = metadata
        self.extract_metadata = extract_metadata

    def call_inspect4py(self, input_path: str, output_path: str) -> str:
        """Call inspect4py for code analysis and extraction.

        Args:
            input_path (str): The path of the repository
            output_path (str): The path to output inspect4py to.

        Returns:
            output_path (str)
        """
        log.info(
            "Extracting information from %s using inspect4py to %s...",
            input_path,
            output_path,
        )

        try:
            args = [
                    "inspect4py",
                    "-i",
                    input_path,
                    "-o",
                    output_path,
                    "-rm",
                    "-si",
                    "-ld",
                    "-sc",
                    "-ast",
                    "-dt",
                    "-cl",
                ]

            if self.extract_metadata:
                args.append("-md")

            subprocess.check_output(args)
        except subprocess.CalledProcessError as e:
            log.critical(e)
            raise e

        log.info("Done!")
        return output_path

    @staticmethod
    def parse_inspect4py_output(path) -> Tuple[dict[str, Any], dict[str, Any]]:
        """Parse the output directory of inspect4py.

        Args:
            path (str): Path to the output directory.

        Returns:
            dict[str, Any]: directory_info.json
            dict[str, Any]: call_graph.json
        """
        di = None
        cg = None

        try:
            di = read_json_from_file(os.path.join(path, "directory_info.json"))
        except FileNotFoundError:
            log.error("Couldn't find directory_info.json in input directory!")

        try:
            cg = read_json_from_file(os.path.join(path, "call_graph.json"))
        except FileNotFoundError:
            log.error("Couldn't find call_graph.json in input directory!")

        return di, cg

    @staticmethod
    def cleanup_inspect4py_output() -> None:
        """Remove the temporary inspect4py output folder

        Returns:
            None
        """
        log.info("Cleaning up temporary directory...")
        shutil.rmtree("./tmp", ignore_errors=True)
        log.info("Done!")

    def build(
        self,
        input_list: List[str],
        name: str,
        description: str,
        prune: bool = False,
    ) -> None:
        """Build a  graph using the input repositories.

        Args:
            input_list (List[str]): The list of paths to repositories to add the graph.
            name (str): The name to assign to the graph.
            description (str): The description to associate with the graph.
            prune (bool): Whether to prune existing nodes from the graph.

        Returns:
            None
        """
        failure = 0
        success = 0

        if prune:
            log.info("Pruning existing graph...")
            self.graph.delete_graph(name.lower())

        with self.graph.get_system_transaction() as (system_tx, metadata_tx):
            graph = self.graph.create_graph(name, description, system_tx, metadata_tx)

        for i in input_list:
            with self.graph.get_transaction(graph.neo4j_name) as tx:
                try:
                    self.call_inspect4py(i, self.temp_output)
                    directory_info, call_graph = self.parse_inspect4py_output(
                        self.temp_output
                    )

                    # Attempt to parse requirements
                    try:
                        requirements = find_requirements(i)
                    except Exception as e:
                        log.error("Error passing requirements: %s", e)
                        requirements = []

                    builder = RepographBuilder(
                        self.summarization.summarize_function
                        if self.summarization.active
                        else None,
                        self.temp_output,
                        graph.neo4j_name,
                        self.graph,
                        tx,
                    )

                    builder.build(directory_info, call_graph, requirements=requirements)

                    log.info("Done!")

                    success += 1
                except subprocess.CalledProcessError as e:
                    log.error("Error invoking inspect4py - %s", str(e))
                    failure += 1
                    raise e
                except RepographBuildError as e:
                    log.error("Error building repograph - %s", str(e))
                    failure += 1
                    raise e
                finally:
                    self.cleanup_inspect4py_output()

        if success == 0:
            self.graph.delete_graph(graph.neo4j_name)
        else:
            self.metadata.set_graph_status_to_created(graph)

        log.info(
            "Parsed %d repositories successfully with %d failures (%d total)",
            success,
            failure,
            len(input_list),
        )
