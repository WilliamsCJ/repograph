"""

"""
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Container


# Containers
from repograph.entities.build.container import BuildContainer
from repograph.entities.graph.container import GraphContainer
# from repograph.entities.management.container import ManagementContainer
from repograph.entities.summarization.container import SummarizationContainer


class ApplicationContainer(DeclarativeContainer):
    """Top-level container
    This container wires together all other containers to bring together the application.
    """
    wiring_config: WiringConfiguration = WiringConfiguration(
        modules=[
            "repograph.cli"
        ]
    )

    # Containers
    graph: Container[GraphContainer] = Container(
        GraphContainer
    )

    summarization: Container[SummarizationContainer] = Container(
        SummarizationContainer
    )

    build: Container[BuildContainer] = Container(
        BuildContainer,
        graph=graph.container.service,
        summarization=summarization.container.service
    )
