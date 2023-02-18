# pragma: no cover
"""
Application-level Container for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Configuration, Resource
from py2neo import GraphService
from neo4j import GraphDatabase, Driver


# Containers
from repograph.entities.build.container import BuildContainer
from repograph.entities.graph.container import GraphContainer
from repograph.entities.search.container import SearchContainer
from repograph.entities.summarization.container import SummarizationContainer
from repograph.entities.metadata.container import MetadataContainer


class ApplicationContainer(DeclarativeContainer):
    """Top-level container
    This container wires together all other containers to bring together the application.
    """

    # Configuration object
    config = Configuration()

    print(config.uri)

    # Neo4j resource
    neo4j: Resource[GraphService] = Resource(
        # GraphService,
        # config.uri,
        # auth=("neo4j", "s3cr3t"),
        GraphService,
        "bolt://localhost:7687",
        auth=("neo4j", "s3cr3t"),
    )

    # Manual Neo4j driver
    driver: Resource[Driver] = Resource(
        # GraphDatabase.driver,
        # config.driver_uri,
        # auth=("neo4j", "s3cr3t")
        GraphDatabase.driver,
        "bolt://localhost:7687",
        auth=("neo4j", "s3cr3t"),
    )

    # Container for Metadata entity
    metadata: Container[MetadataContainer] = Container(
        MetadataContainer,
        config=config,
    )

    # Container for Graph entity
    graph: Container[GraphContainer] = Container(
        GraphContainer,
        neo4j=neo4j.provided,
        driver=driver.provided,
        metadata=metadata.container.service,
    )

    # Container for Summarization entity
    summarization: Container[SummarizationContainer] = Container(
        SummarizationContainer, config=config
    )

    # Container for Build entity
    build: Container[BuildContainer] = Container(
        BuildContainer,
        graph=graph.container.service,
        summarization=summarization.container.service,
        config=config,
        metadata=metadata.container.service,
    )

    # Container for Search entity
    search: Container[SearchContainer] = Container(
        SearchContainer, config=config, graph=graph.container.service
    )
