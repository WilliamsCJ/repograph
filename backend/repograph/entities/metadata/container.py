# pragma: nocover
"""
Container for metadata entity for dependency injection.
"""
# Base imports
from sqlite3 import Connection

# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Singleton

# Summarize entity imports
from repograph.entities.metadata.repository import MetadataRepository
from repograph.entities.metadata.service import MetadataService


class MetadataContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    sqlite: Dependency[Connection] = Dependency()

    repository: Singleton[MetadataRepository] = Singleton(
        MetadataRepository,
        db=sqlite
    )

    service: Singleton[MetadataService] = Singleton(
        MetadataService,
        repository=repository
    )
