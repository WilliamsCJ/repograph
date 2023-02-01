""""
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


class BuildContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    graph: Dependency[GraphService] = Dependency()

    summarization: Dependency[SummarizationService] = Dependency()

    service: Singleton[BuildService] = Singleton(
        BuildService,
        graph=graph,
        summarization=summarization
    )

    router: Singleton[BuildRouter] = Singleton(
        BuildRouter,
        service=service
    )
