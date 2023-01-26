""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository
from repograph.entities.graph.service import GraphService


class GraphContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    repository: Singleton[GraphRepository] = Singleton(
        GraphRepository,
        uri=config.uri,
        user=config.user,
        password=config.user,
        database=config.database
    )

    service: Singleton[GraphService] = Singleton(
        GraphService,
        repository=repository
    )
