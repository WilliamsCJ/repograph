"""
Graph entity application logic.
"""
# Base imports
import contextlib
import datetime
import traceback
from logging import getLogger
import re
from sqlite3 import Connection
from typing import Dict, List

# pip imports
from py2neo import Transaction
from neo4j import Transaction as neo4jTransaction

# Model imports
from repograph.entities.graph.models.base import BaseSubgraph, Node, Relationship
from repograph.entities.graph.models.nodes import (
    Class,
    Docstring,
    Function,
    Module,
    Package,
    Repository,
)
from repograph.entities.graph.models.graph import GraphSummary, CallGraph

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository

# Metadata entity imports
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.service import MetadataService

# Exceptions
from repograph.entities.graph.exceptions import InvalidGraphNameError

# Configure logging
log = getLogger("repograph.entities.graph.service")


class GraphService:
    """
    The GraphService class implements all application-logic related to the graph entity.
    """

    repository: GraphRepository
    metadata: MetadataService

    def __init__(self, repository: GraphRepository, metadata: MetadataService):
        """Constructor

        Args:
            repository (GraphRepository): The Neo4j graph repository.
            metadata (MetadataService): The metadata service.
        """
        self.repository = repository
        self.metadata = metadata

    def create_graph(
        self,
        name: str,
        description: str,
        system_tx: neo4jTransaction,
        metadata_tx: Connection,
    ) -> Graph:
        """Create a new graph.

        Args:
            name:
            description:
            system_tx:
            metadata_tx:

        Returns:
            Graph: Created Graph object
        """
        if not re.match(r"^[a-z,A-Z,0-9][a-z,A-Z,0-9]{2,63}$", name.lower()):
            raise InvalidGraphNameError(name)

        graph = Graph(
            neo4j_name=name.lower(),
            name=name,
            description=description,
            created=datetime.datetime.now(),
        )

        self.repository.create_graph(graph.neo4j_name, system_tx)
        self.metadata.register_graph(graph, metadata_tx)

        return graph

    def delete_graph(self, name: str) -> None:
        """Delete a graph

        Args:
            name (str): Name of the graph to delete

        Returns:
            None
        """
        self.repository.delete_graph(name)
        self.metadata.delete_graph(name)

    @contextlib.contextmanager
    def get_transaction(self, graph_name):
        """Obtain a Neo4j transaction for a given graph.

        Args:
            graph_name (str): The name of the graph
        """
        tx = self.repository.get_transaction(graph_name=graph_name)
        try:
            yield tx
            log.info("Committing changes to graph...")
            tx.commit()
            log.info("Done!")
        except Exception as e:
            log.error("An error occurred. Rolling back graph transaction!\n" + str(e))
            traceback.print_exc()
            tx.rollback()

    @contextlib.contextmanager
    def get_system_transaction(self):
        tx = self.repository.get_driver_transaction()
        metadata_tx = self.metadata.get_transaction()
        try:
            yield tx, metadata_tx
            tx.commit()
            metadata_tx.commit()
        except Exception as e:
            log.error(
                "An error occurred. Rolling back system graph and metadata transactions!\n%s",
                str(e),
            )
            tx.rollback()
            metadata_tx.rollback()
            raise e

    def add(self, *args: BaseSubgraph, tx: Transaction = None, graph_name=None):
        """Add nodes/relationships to the graph

        Args:
            *args (BaseSubgraph): Nodes and/or relationships
            tx (Transaction): The optional transaction object to use
            graph_name (str): The optional graph name to obtain a transaction for if no tx is used.
        """
        self.repository.add(*args, tx=tx, graph_name=graph_name)

    def bulk_add(
        self, nodes: List[Node], relationships: List[Relationship], graph_name: str
    ):
        """Bulk add nodes and relationships.

        Args:
            nodes (List[Node]): Nodes to add.
            relationships (List[Relationship]): Relationships to add.
            graph_name (str): The optional graph name to obtain a transaction for.

        Return:
            None
        """
        self.repository.add(*nodes, *relationships, graph_name=graph_name)

    def get_summary(self, graph_name: str) -> GraphSummary:
        """Calculate a summary of the graph.

        Args:
            graph_name (str): The graph name to get summary for.

        Return:
            GraphSummary
        """
        if not self.repository.has_nodes(graph_name=graph_name):
            log.warning("Graph has no nodes")
            return GraphSummary()

        summary = GraphSummary(is_empty=False)

        # Nodes and relationships totals
        nodes, relationships = self.repository.get_number_of_nodes_and_relationships(
            graph_name=graph_name
        )
        summary.nodes_total = nodes
        summary.relationships_total = relationships

        # Repositories
        summary.repositories = len(
            self.repository.get_all_nodes_by_label(Repository, graph_name=graph_name)
        )

        # Packages
        summary.packages = len(
            self.repository.get_all_nodes_by_label(Package, graph_name=graph_name)
        )

        # Modules
        summary.modules = len(
            self.repository.get_all_nodes_by_label(Module, graph_name=graph_name)
        )

        # Classes
        summary.classes = len(
            self.repository.get_all_nodes_by_label(Class, graph_name=graph_name)
        )

        # Functions
        summary.functions = len(
            self.repository.get_all_nodes_by_label(Function, graph_name=graph_name)
        )

        return summary

    def get_docstrings(self, graph: str):
        return self.repository.get_all_nodes_by_label(Docstring, graph_name=graph)

    def get_function_summarizations(
        self, graph_name: str, repository_name: str = None
    ) -> Dict[str, Function]:
        """Converts all Function nodes into a list of tuples.

        Args:
            graph_name (str): The graph name to get function summarizations for.
            repository_name (str, optional): The specific repository within the
                                             graph to search against.

        Returns:
            List[Tuple[str, Function]
        """
        if not repository_name:
            repository_name = ".*"

        nodes = self.repository.execute_query(
            f"""
            MATCH (n:Docstring)-[:Documents]-(f:Function) WHERE n.summarization IS NOT NULL
            AND f.repository =~ {repository_name}
            RETURN n.summarization as `summarization`, f as `function`
            """,
            graph_name=graph_name,
        )

        return dict(
            map(
                lambda x: (
                    x["summarization"],
                    Function(identity=x["function"].identity, **x["function"]),
                ),
                nodes,
            )
        )

    def get_call_graph_by_id(self, node_id: int, graph_name: str) -> CallGraph:
        """Get the call graph for a Function node by its ID.

        Args:
            node_id (int): ID of the Function node.
            graph_name (str): The graph name to get function summarizations for.

        Returns:
            CallGraph
        """
        results = self.repository.execute_query(
            f"""
            MATCH (c:Function)-[r:Calls*0..1]-(f:Function) WHERE ID(f) = {node_id}
            RETURN f as `function`, c as `call`, r as `relationship`
            """,
            graph_name=graph_name,
        )

        call_graph = CallGraph()

        call_graph.nodes.append(
            CallGraph.Function(
                id=results[0]["function"].identity,
                label=results[0]["function"]["canonical_name"],
                title=results[0]["function"]["canonical_name"],
            )
        )

        results = list(filter(lambda x: x["call"].identity != node_id, results))
        if len(results) == 0:
            return call_graph

        call_graph.nodes.extend(
            list(
                map(
                    lambda res: CallGraph.Function(
                        id=res["call"].identity,
                        label=(
                            res["call"]["canonical_name"]
                            if "canonical_name" in res
                            else res["call"]["name"]
                        ),
                        title=(
                            res["call"]["canonical_name"]
                            if "canonical_name" in res
                            else res["call"]["name"]
                        ),
                    ),
                    results,
                )
            )
        )

        def parse_relationships(x):
            return list(
                map(
                    lambda y: CallGraph.Relationship(
                        from_id=y.start_node.identity,
                        to_id=y.end_node.identity,
                    ),
                    x["relationship"],
                )
            )

        call_graph.edges.extend(
            [
                item
                for sublist in list(map(parse_relationships, results))
                for item in sublist
            ]
        )

        return call_graph

    def get_cyclical_dependencies(self, graph: str) -> int:
        """Get the number of cyclical dependencies in the specified graph.

        Args:
            graph (str): The name of the graph to check.

        Returns:
            int: The number of unique cyclical dependencies.
        """
        result = self.repository.execute_query(
            "MATCH p=(n)-[:Imports|Calls*]->(n) RETURN nodes(p) as `nodes`",
            graph_name=graph,
        )

        cycles = set()

        for cycle in result:
            cycles.add(frozenset(map(lambda x: x.identity, cycle.get("nodes"))))

        return len(cycles)

    def get_missing_dependencies(self, graph: str) -> int:
        """Get the number of dependencies that are missing from the requirements.

        Args:
            graph (str): The name of the graph to check.

        Returns:
            int: The number of unique packages (inferred) that have no relationship to
                 the Repository node(s).
        """
        result = self.repository.execute_query(
            "MATCH (n:Package) WHERE (n.inferred) = true AND  NOT (n)-[*]->(:Repository) RETURN DISTINCT n",
            graph_name=graph,
        )

        return len(result)
