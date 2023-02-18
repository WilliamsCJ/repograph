# pragma: no cover
"""
Container for graph entity for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from py2neo import GraphService as py2neoGraphService
from neo4j import Driver

# Graph entity imports
from repograph.entities.graph.repository import GraphRepository
from repograph.entities.graph.router import GraphRouter
from repograph.entities.graph.service import GraphService

# Metadata entity imports
from repograph.entities.metadata.service import MetadataService


class GraphContainer(DeclarativeContainer):
    neo4j: Dependency[py2neoGraphService] = Dependency()

    driver: Dependency[Driver] = Dependency()

    metadata: Dependency[MetadataService] = Dependency()

    repository: Singleton[GraphRepository] = Singleton(
        GraphRepository, graph=neo4j, driver=driver
    )

    service: Singleton[GraphService] = Singleton(
        GraphService, repository=repository, metadata=metadata
    )

    router: Singleton[GraphRouter] = Singleton(GraphRouter, service=service)
