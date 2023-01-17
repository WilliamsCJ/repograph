"""

"""
import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Resource

from repograph.repograph import Repograph


class ApplicationContainer(DeclarativeContainer):
    """Top-level container
    This container wires together all other containers to bring together the application.
    """
    wiring_config: WiringConfiguration = WiringConfiguration(
        packages=[
            ".routers",
        ],
    )

    repograph: Resource[Repograph] = Resource(
        Repograph,
        os.environ.get("NEO4J_URI"),
        os.environ.get("NEO4J_USER"),
        os.environ.get("NEO4J_PASSWORD"),
        os.environ.get("NEO4J_DATABASE")
    )
