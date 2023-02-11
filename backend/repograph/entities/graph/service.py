"""
Graph entity application logic.
"""
import contextlib
import datetime
# Base imports
from logging import getLogger
from py2neo import Transaction
from typing import Dict, List

# Model imports
from repograph.entities.graph.models.base import BaseSubgraph, Node, Relationship
from repograph.entities.graph.models.nodes import Class, Function, Module, Package, Repository
from repograph.entities.graph.models.graph import GraphSummary, CallGraph

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository

# Metadata entity imports
from repograph.entities.metadata.models import Graph
from repograph.entities.metadata.service import MetadataService

# Configure logging
log = getLogger('repograph.entities.graph.service')


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

    def create_graph(self, name: str, description: str):
        graph = Graph(
            neo4j_name=name.lower(),
            name=name,
            description=description,
            created=datetime.datetime.now()
        )

        self.repository.create_graph(graph.neo4j_name)
        self.metadata.register_graph(graph)

        return graph

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
            tx.rollback()

    def add(self, *args: BaseSubgraph, tx: Transaction = None, graph_name=None):
        """Add nodes/relationships to the graph

        Args:
            *args (BaseSubgraph): Nodes and/or relationships
            tx (Transaction): The optional transaction object to use
            graph_name (str): The optional graph name to obtain a transaction for if no tx is used.
        """
        self.repository.add(*args, tx=tx, graph_name=graph_name)

    def bulk_add(self, nodes: List[Node], relationships: List[Relationship], graph_name: str):
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
        if not self.repository.has_nodes():
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
        summary.repositories = len(self.repository.get_all_nodes_by_label(
            Repository, graph_name=graph_name
        ))

        # Packages
        summary.packages = len(self.repository.get_all_nodes_by_label(
            Package, graph_name=graph_name
        ))

        # Modules
        summary.modules = len(self.repository.get_all_nodes_by_label(
            Module, graph_name=graph_name
        ))

        # Classes
        summary.classes = len(self.repository.get_all_nodes_by_label(
            Class, graph_name=graph_name
        ))

        # Functions
        summary.functions = len(self.repository.get_all_nodes_by_label(
            Function, graph_name=graph_name
        ))

        return summary

    def get_function_summarizations(
            self,
            graph_name: str,
            repository_name: str = None
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
            repository_name = '.*'

        nodes = self.repository.execute_query(
            f"""
            MATCH (n:Docstring)-[:Documents]-(f:Function) WHERE n.summarization IS NOT NULL
            AND f.repository =~ {repository_name}
            RETURN n.summarization as `summarization`, f as `function`
            """,
            graph_name=graph_name
        )

        return dict(map(lambda x: (x['summarization'], Function(identity=x['function'].identity, **x['function'])), nodes))  # noqa: 501

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
            graph_name=graph_name
        )

        call_graph = CallGraph()

        call_graph.nodes.append(CallGraph.Function(
            id=results[0]["function"].identity,
            label=results[0]["function"]["canonical_name"],
            title=results[0]["function"]["canonical_name"]
        ))

        results = list(filter(lambda x: x["call"].identity != node_id, results))
        if len(results) == 0:
            return call_graph

        call_graph.nodes.extend(list(map(lambda res: CallGraph.Function(
            id=res["call"].identity,
            label=(res["call"]["canonical_name"] if "canonical_name" in res else res["call"]["name"]),  # noqa: 501
            title=(res["call"]["canonical_name"] if "canonical_name" in res else res["call"]["name"])  # noqa: 501
        ), results)))

        def parse_relationships(x):
            return list(map(lambda y: CallGraph.Relationship(
                from_id=y.start_node.identity,
                to_id=y.end_node.identity,
            ), x["relationship"]))

        call_graph.edges.extend(
            [item for sublist in list(map(parse_relationships, results)) for item in sublist]
        )

        return call_graph

    def prune(self, graph_name: str):
        """Delete all nodes and relationships from the graph.

        Also free up the name for reuse.

        Args:
            graph_name (str): The name of the graph to delete.

        """
        self.repository.delete_graph(graph_name)
