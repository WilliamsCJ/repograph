"""
Neo4J Graph Database related functionality.
"""
import logging
from py2neo import Graph

log = logging.getLogger('repograph.utils.neo4j')


def create_indices(graph: Graph) -> None:
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Function) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Module) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Package) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Class) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Repository) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:README) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Directory) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:Variable) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:License) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringArgument) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringReturnValue) ON (n.graphName)")
    graph.run("CREATE TEXT INDEX IF NOT EXISTS for (n:DocstringRaises) ON (n.graphName)")

    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Function) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Module) ON (n.graphName, n.repositoryName)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Package) ON (n.graphName, n.repositoryName)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Class) ON (n.graphName, n.repositoryName)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Repository) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:README) ON (n.graphName, n.repositoryName)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Directory) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:Variable) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:License) ON (n.graphName, n.repositoryName)")
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringArgument) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringReturnValue) ON (n.graphName, n.repositoryName)")  # noqa: 501
    graph.run("CREATE RANGE INDEX IF NOT EXISTS for (n:DocstringRaises) ON (n.graphName, n.repositoryName)")  # noqa: 501
