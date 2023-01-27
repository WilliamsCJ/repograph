""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from py2neo import Graph

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository
from repograph.entities.graph.service import GraphService


class GraphContainer(DeclarativeContainer):
    neo4j: Dependency[Graph] = Dependency()

    repository: Singleton[GraphRepository] = Singleton(
        GraphRepository,
        graph=neo4j
    )

    service: Singleton[GraphService] = Singleton(
        GraphService,
        repository=repository
    )
