"""
API entrypoint.
"""
# Base imports
import logging

# pip imports
from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from repograph.container import ApplicationContainer

log = logging.getLogger('repograph.api')


@inject
def create_app() -> FastAPI:
    """Creates FastAPI application.
    Returns:
        FastAPI: Initialised FastAPI application object.
    """
    container = ApplicationContainer()
    container.init_resources()

    application = FastAPI(
        title="Repograph",
        description="Backend API",
        openapi_url="/v1/openapi.json",
        docs_url="/v1/docs",
        redoc_url="/v1/docs"
    )

    application.include_router(container.graph.container.router)

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
    container.wire(modules=[__name__])

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=3000)
