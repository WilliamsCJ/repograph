"""
Graph entity application logic.
"""
# Base imports
from logging import getLogger
from typing import Dict, List

# Model imports
from repograph.models.base import Node, Relationship
from repograph.models.nodes import Class, Function, Module, Repository
from repograph.models.graph import GraphSummary, CallGraph

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository

# Configure logging
log = getLogger('repograph.entities.graph.service')


class GraphService:
    """
    The GraphService class implements all application-logic related to the graph entity.
    """
    repository: GraphRepository

    def __init__(self, repository: GraphRepository):
        """Constructor

        Args:
            repository (GraphRepository): The Neo4j graph repository.
        """
        self.repository = repository

    def bulk_add(self, nodes: List[Node], relationships: List[Relationship]):
        """Bulk add nodes and relationships.

        Args:
            nodes (List[Node]): Nodes to add.
            relationships (List[Relationship]): Relationships to add.

        Return:
            None
        """
        self.repository.add(*nodes, *relationships)

    def get_summary(self) -> GraphSummary:
        """Calculate a summary of the graph.

        Return:
            GraphSummary
        """
        if not self.repository.has_nodes():
            log.warning("Graph has no nodes")
            return GraphSummary()

        summary = GraphSummary(is_empty=False)

        # Nodes and relationships totals
        nodes, relationships = self.repository.get_number_of_nodes_and_relationships()
        summary.nodes_total = nodes
        summary.relationships_total = relationships

        # Repositories
        _, count = self.repository.get_all_nodes_by_label(Repository)
        summary.repositories = count

        # Modules
        _, count = self.repository.get_all_nodes_by_label(Module)
        summary.modules = count

        # Classes
        _, count = self.repository.get_all_nodes_by_label(Class)
        summary.classes = count

        # Functions
        _, count = self.repository.get_all_nodes_by_label(Function)
        summary.functions = count

        return summary

    def get_function_summarizations(self) -> Dict[str, Function]:
        """Converts all Function nodes into a list of tuples.

        Tuple: (summarization, node)

        Returns:
            List[Tuple[str, Function]
        """
        nodes = self.repository.execute_query(
            """
            MATCH (n:Docstring)-[:Documents]-(f:Function) WHERE n.summarization IS NOT NULL
            RETURN n.summarization as `summarization`, f as `function`
            """
        )

        return dict(map(lambda x: (x['summarization'], Function(identity=x['function'].identity, **x['function'])), nodes))  # noqa: 501

    def get_call_graph_by_id(self, node_id: int) -> CallGraph:
        results = self.repository.execute_query(
            f"""
            MATCH (c:Function)-[r:Calls*0..1]-(f:Function) WHERE ID(f) = {node_id}
            RETURN f as `function`, c as `call`, r as `relationship`
            """
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

    def prune(self):
        """Delete all nodes and relationships from the graph."""
        self.repository.delete_all()
