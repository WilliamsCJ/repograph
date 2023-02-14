# pragma: no cover
"""
Container for metadata entity for dependency injection.
"""
# pip imports
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

# Summarize entity imports
from repograph.entities.metadata.repository import MetadataRepository
from repograph.entities.metadata.router import MetadataRouter
from repograph.entities.metadata.service import MetadataService


class MetadataContainer(DeclarativeContainer):
    config: Configuration = Configuration()

    repository: Singleton[MetadataRepository] = Singleton(
        MetadataRepository,
        db_path=config.metadata_db
    )

    service: Singleton[MetadataService] = Singleton(
        MetadataService,
        repository=repository
    )

    router: Singleton[MetadataRouter] = Singleton(
        MetadataRouter,
        service=service
    )
