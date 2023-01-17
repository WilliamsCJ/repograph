"""
Graph-related routers.
"""
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status

from repograph.api.containers import ApplicationContainer
from repograph.repograph import Repograph
from repograph.models.repograph import RepographSummary

repograph_service: Provide = Provide[ApplicationContainer.repograph]

graphRouter = APIRouter(
    prefix="/graph",
    tags=["Graph"],
    responses={}
)


@graphRouter.get(
    "/summary",
    response_model=RepographSummary,
    status_code=status.HTTP_200_OK
)
@inject
async def get_summary(repograph: Repograph = Depends(repograph_service)):
    return repograph.get_summary()
