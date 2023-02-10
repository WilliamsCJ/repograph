""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from py2neo import GraphService as py2neoGraphService

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository
from repograph.entities.graph.router import GraphRouter
from repograph.entities.graph.service import GraphService


class GraphContainer(DeclarativeContainer):
    neo4j: Dependency[py2neoGraphService] = Dependency()

    repository: Singleton[GraphRepository] = Singleton(
        GraphRepository,
        graph=neo4j
    )

    service: Singleton[GraphService] = Singleton(
        GraphService,
        repository=repository
    )

    router: Singleton[GraphRouter] = Singleton(
        GraphRouter,
        service=service
    )
