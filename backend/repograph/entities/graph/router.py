"""
Routing for build entity.
"""
# pip imports
from fastapi import APIRouter, status

# Model imports
from repograph.entities.graph.models.graph import CallGraph

# Graph entity imports
from repograph.entities.graph.service import GraphService


class GraphRouter:
    service: GraphService

    def __init__(self, service: GraphService):
        self.service = service

        self.router = APIRouter(prefix="/graph", tags=["Summary"], responses={})

        self.router.add_api_route(
            "/{graph}/summary",
            self.summary,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )

        self.router.add_api_route(
            "/{graph}/node/{node_id}/call_graph",
            self.call_graph_by_id,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
            response_model_by_alias=True,
            response_model=CallGraph,
        )

    async def summary(self, graph: str):
        return self.service.get_summary(graph)

    async def call_graph_by_id(self, graph: str, node_id: int) -> CallGraph:
        return self.service.get_call_graph_by_id(node_id, graph)
