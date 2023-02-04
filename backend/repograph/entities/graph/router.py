"""
Routing for build entity.
"""
# pip imports
from fastapi import APIRouter, status

# Model imports

# Graph entity imports
from repograph.entities.graph.service import GraphService


class GraphRouter:
    service: GraphService

    def __init__(self, service: GraphService):
        self.service = service

        self.router = APIRouter(
            prefix="/graph",
            tags=["Summar"],
            responses={}
        )

        self.router.add_api_route(
            "/{graph}/summary",
            self.summary,
            methods=["GET"],
            status_code=status.HTTP_200_OK
        )

    async def summary(self, graph: str):
        return self.service.get_summary()
