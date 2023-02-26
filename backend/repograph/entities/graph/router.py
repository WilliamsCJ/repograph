"""
Routing for build entity.
"""
# Base imports
from typing import List

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

        self.router.add_api_route(
            "/{graph}",
            self.delete_graph,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

        self.router.add_api_route(
            "/{graph}/cylical-dependencies",
            self.cyclical_dependencies,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )

        self.router.add_api_route(
            "/{graph}/missing-dependencies",
            self.missing_dependencies,
            methods=["GET"],
            status_code=status.HTTP_200_OK,
        )

        self.router.add_api_route(
            "/{graph}/repositories", self.get_repositories, methods=["GET"]
        )

    async def summary(self, graph: str):
        return self.service.get_summary(graph)

    async def cyclical_dependencies(self, graph: str):
        return self.service.get_cyclical_dependencies(graph)

    async def missing_dependencies(self, graph: str):
        return self.service.get_missing_dependencies(graph)

    async def call_graph_by_id(self, graph: str, node_id: int) -> CallGraph:
        return self.service.get_call_graph_by_id(node_id, graph)

    async def get_repositories(self, graph: str) -> List[str]:
        return self.service.get_repository_names(graph)

    async def delete_graph(self, graph: str):
        self.service.delete_graph(graph)
