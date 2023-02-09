"""
Neo4J Graph Database related functionality.
"""
import logging
from py2neo import Graph

log = logging.getLogger('repograph.utils.neo4j')


def create_indices(graph: Graph) -> None:
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Function) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Module) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Package) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Class) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Repository) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:README) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Directory) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Variable) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:License) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringArgument) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringReturnValue) ON (n.graph_name)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringRaises) ON (n.graph_name)")

    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Function) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Module) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Package) ON (n.graph_name, n.repository_name)")   # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Class) ON (n.graph_name, n.repository_name)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Repository) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:README) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Directory) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Variable) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:License) ON (n.graph_name, n.repository_name)")   # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringArgument) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringReturnValue) ON (n.graph_name, n.repository_name)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringRaises) ON (n.graph_name, n.repository_name)")  # noqa: 501
