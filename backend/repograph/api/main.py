"""
API Main
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from repograph.api.routers import base_router
from repograph.api.containers import ApplicationContainer

log = logging.getLogger('repograph.api')


def create_app() -> FastAPI:
    """Creates FastAPI application.
    Returns:
        FastAPI: Initialised FastAPI application object.
    """
    container = ApplicationContainer()
    container.init_resources()

    application = FastAPI(
        title="",
        description="",
        openapi_url="/v1/openapi.json",
        docs_url="/v1/docs",
        redoc_url="/v1/docs"
    )

    application.container = container

    application.include_router(base_router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return application


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=3000)
