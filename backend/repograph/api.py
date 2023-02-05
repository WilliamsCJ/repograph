"""
API entrypoint.
"""
# Base imports
import logging

# pip imports
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Application Container
from repograph.container import ApplicationContainer

# Entity imports
from repograph.entities.graph.router import GraphRouter
from repograph.entities.search.router import SearchRouter

# Utilities
from repograph.utils.exception_handlers import generic_exception_handler
from repograph.utils.logging import configure_logging

# Configure logging format
configure_logging()
log = logging.getLogger('repograph.api')


@inject
def create_app(
    graph_router: GraphRouter = Provide[ApplicationContainer.graph.container.router],
    search_router: SearchRouter = Provide[ApplicationContainer.search.container.router]
) -> FastAPI:
    """Creates FastAPI application.

    Args:
        graph_router (GraphRouter): The graph entity router.
        search_router (SearchRouter): The search entity router.

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

    # Configure CORS, https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Add exception handlers
    application.add_exception_handler(Exception, generic_exception_handler)

    return application


# if __name__ == "__main__":
container = ApplicationContainer()
container.config.from_yaml("../config.yaml")
container.init_resources()
container.wire(modules=[__name__])

app = create_app()
# uvicorn.run("repograph.api:app", host="0.0.0.0", port=3000, reload=True)
