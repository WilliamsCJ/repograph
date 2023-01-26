"""

"""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Container, Configuration


# Containers
from repograph.entities.build.container import BuildContainer
from repograph.entities.graph.container import GraphContainer
# from repograph.entities.management.container import ManagementContainer
from repograph.entities.summarization.container import SummarizationContainer


class ApplicationContainer(DeclarativeContainer):
    """Top-level container
    This container wires together all other containers to bring together the application.
    """
    # Configuration object
    config = Configuration()

    # Wiring for dependency injection
    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "repograph.cli"
        ]
    )

    # Container for Graph entity
    graph: Container[GraphContainer] = Container(
        GraphContainer,
        config=config
    )

    # Container for Summarization entity
    summarization: Container[SummarizationContainer] = Container(
        SummarizationContainer,
        config=config
    )

    # Container for Build entity
    build: Container[BuildContainer] = Container(
        BuildContainer,
        graph=graph.container.service,
        summarization=summarization.container.service,
        config=config
    )
