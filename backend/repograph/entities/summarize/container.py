""""
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

# Summarize entity imports
from repograph.entities.summarize.service import SummarizationService


class SummarizationContainer(DeclarativeContainer):
    summarization_service: Singleton[SummarizationService] = Singleton(
        SummarizationService,
    )
