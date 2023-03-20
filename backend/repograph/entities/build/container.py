# pragma: no cover
"""
Container for build entity for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Singleton

# Build entity imports
from repograph.entities.build.service import BuildService
from repograph.entities.build.router import BuildRouter

# Other entity imports
from repograph.entities.graph.service import GraphService
from repograph.entities.summarization.service import SummarizationService
from repograph.entities.metadata.service import MetadataService


class BuildContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    graph: Dependency[GraphService] = Dependency()

    summarization: Dependency[SummarizationService] = Dependency()

    metadata: Dependency[MetadataService] = Dependency()

    service: Singleton[BuildService] = Singleton(
        BuildService,
        graph=graph,
        summarization=summarization,
        metadata=metadata,
        extract_metadata=config.extract_metadata
    )

    router: Singleton[BuildRouter] = Singleton(
        BuildRouter,
        service=service
    )
