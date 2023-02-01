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
from repograph.entities.build.utils import read_json_from_file

# Other service imports
from repograph.entities.graph.service import GraphService
from repograph.entities.summarization.service import SummarizationService


# Configure logging
log = getLogger('repograph.entities.build.service')


class BuildService:
    graph: GraphService
    summarization: SummarizationService

    temp_output = "./tmp"

    def __init__(
        self,
        graph: GraphService,
        summarization: SummarizationService
    ):
        """Constructor

        Args:
            graph (GraphService): The Graph Service.
            summarization (SummarizationService): The Summarization Service
        """
        self.graph = graph
        self.summarization = summarization

    @staticmethod
    def call_inspect4py(input_path: str, output_path: str) -> str:
        """Call inspect4py for code analysis and extraction.

        Args:
            input_path (str): The path of the repository
            output_path (str): The path to output inspect4py to.

        Returns:
            output_path (str)
        """
        log.info("Extracting information from %s using inspect4py...", input_path)

        subprocess.check_call([
            "inspect4py",
            "-i",
            input_path,
            "-o",
            output_path,
            "-md",
            "-rm",
            "-si",
            "-ld",
            "-sc",
            "-ast",
            # "-r",
            "-cl"
        ])

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
        shutil.rmtree("./tmp")
        log.info("Done!")

    def build(
        self,
        input_list: List[str],
        prune: bool = False
    ) -> None:
        """Build a  graph using the input repositories.

        Args:
            input_list (List[str]): The list of paths to repositories to add the graph.
            prune (bool): Whether to prune existing nodes from the graph.

        Returns:
            None
        """
        failure = 0
        success = 0

        if prune:
            log.info("Pruning existing nodes...")
            self.graph.prune()

        for i in input_list:
            try:
                self.call_inspect4py(i, self.temp_output)
                directory_info, call_graph = self.parse_inspect4py_output(self.temp_output)

                builder = RepographBuilder(
                    summarize=self.summarization.summarize_function if self.summarization.active else None,  # noqa: 501
                    base_path=self.temp_output
                )
                nodes, relationships = builder.build(directory_info, call_graph)

                log.info("Writing nodes and relationships to graph...")
                self.graph.bulk_add(nodes, relationships)
                log.info("Done!")

                success += 1
            except subprocess.CalledProcessError as e:
                log.error("Error invoking inspect4py - %s", str(e))
                failure += 1
            except RepographBuildError as e:
                log.error("Error building repograph - %s", str(e))
                failure += 1
            finally:
                self.cleanup_inspect4py_output()
                pass

        log.info(
            "Parsed %d repositories successfully with %d failures (%d total)",
            success,
            failure,
            len(input_list)
        )
