# pragma: nocover
"""
Container for build entity for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

# Summarize entity imports
from repograph.entities.summarization.service import SummarizationService


class SummarizationContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    service: Singleton[SummarizationService] = Singleton(
        SummarizationService,
        summarize=config.summarize
    )
