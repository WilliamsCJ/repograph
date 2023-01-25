""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Singleton

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository
from repograph.entities.graph.service import GraphService


class GraphContainer(DeclarativeContainer):
    graph_repository: Singleton[GraphRepository] = Singleton(
        GraphRepository,

    )

    graph_service: Singleton[GraphService] = Singleton(
        GraphService,
        repository=graph_repository
    )
