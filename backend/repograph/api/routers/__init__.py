"""
Routers package. Provides API routing.
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from repograph.api.routers.graph import graphRouter

base_router = APIRouter(prefix="/v1")

base_router.include_router(graphRouter)


@base_router.get(
    "/health",
    tags=["General"],
    response_class=JSONResponse
)
def health_check() -> JSONResponse:
    """
    Health check endpoint for monitoring
    """
    return JSONResponse(content={"status": "OK"}, status_code=200)
