# pragma: no cover
"""
API entrypoint.
"""
# Base imports
import logging

# pip imports
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from yaml import UnsafeLoader

# Application Container
from repograph.container import ApplicationContainer

# Entity imports
from repograph.entities.build.router import BuildRouter
from repograph.entities.graph.router import GraphRouter
from repograph.entities.search.router import SearchRouter
from repograph.entities.metadata.router import MetadataRouter

# Utilities
from repograph.utils.exception_handlers import generic_exception_handler
from repograph.utils.logging import configure_logging

# Configure logging format
configure_logging(logging.INFO)
log = logging.getLogger("repograph.api")


@inject
def create_app(
    build_router: BuildRouter = Provide[ApplicationContainer.build.container.router],
    graph_router: GraphRouter = Provide[ApplicationContainer.graph.container.router],
    search_router: SearchRouter = Provide[ApplicationContainer.search.container.router],
    metadata_router: MetadataRouter = Provide[
        ApplicationContainer.metadata.container.router
    ],
) -> FastAPI:
    """Creates FastAPI application.

    Args:
        build_router (BuildRouter): The build entity router.
        graph_router (GraphRouter): The graph entity router.
        search_router (SearchRouter): The search entity router.
        metadata_router (MetadataRouter): The metadata entity router.

    Returns:
        FastAPI: Initialised FastAPI application object.
    """
    # Configure FastAPI application and metadata
    application = FastAPI(
        title="Repograph",
        description="Backend API",
    )

    # Add sub-routers to base router
    application.include_router(graph_router.router)
    application.include_router(search_router.router)
    application.include_router(build_router.router)
    application.include_router(metadata_router.router)
    application.include_router(search_router.graphRouter)

    # Configure CORS, https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add exception handlers
    application.add_exception_handler(Exception, generic_exception_handler)

    return application


container = ApplicationContainer()
container.config.from_yaml("../config.yaml", loader=UnsafeLoader)
container.wire(modules=[__name__])

app = create_app()
