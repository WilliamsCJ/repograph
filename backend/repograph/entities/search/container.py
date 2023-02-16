# pragma: no cover
"""
Container for search entity for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Singleton

# Summarize entity imports
from repograph.entities.search.service import SearchService
from repograph.entities.search.router import SearchRouter

# Graph entity imports
from repograph.entities.graph.service import GraphService


class SearchContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    graph: Dependency[GraphService] = Dependency()

    service: Singleton[SearchService] = Singleton(
        SearchService,
        graph=graph,
    )

    router: Singleton[SearchRouter] = Singleton(
        SearchRouter,
        service=service,
    )
