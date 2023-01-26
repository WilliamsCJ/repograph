""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

# Summarize entity imports
from repograph.entities.summarization.service import SummarizationService


class SummarizationContainer(DeclarativeContainer):
    service: Singleton[SummarizationService] = Singleton(
        SummarizationService,
    )
