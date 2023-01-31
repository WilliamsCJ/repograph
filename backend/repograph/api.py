"""
API entrypoint.
"""
# Base imports
import logging
import sys

# pip imports
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Application Container
from repograph.container import ApplicationContainer

# Entity imports
from repograph.entities.graph.router import GraphRouter

# Utilities
from repograph.utils.logging import configure_logging

# Configure logging format
configure_logging()
log = logging.getLogger('repograph.api')


@inject
def create_app(
    graph_router: GraphRouter = Provide[ApplicationContainer.graph.container.router]
) -> FastAPI:
    """Creates FastAPI application.
    Returns:
        FastAPI: Initialised FastAPI application object.
    """
    application = FastAPI(
        title="Repograph",
        description="Backend API",
        openapi_url="/v1/openapi.json",
        docs_url="/v1/docs",
        redoc_url="/v1/docs"
    )

    application.include_router(graph_router.router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return application


if __name__ == "__main__":
    container = ApplicationContainer()
    container.config.from_yaml(sys.argv[1])
    container.init_resources()
    container.wire(modules=[__name__])

    print(container.config.get("database"))
    print(container.config.get("uri"))
    print(container.config.get("username"))
    print(container.config.get("password"))

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=3000)
