"""
Routing for build entity.
"""
# Base imports
from logging import getLogger
from typing import List

# pip imports
from fastapi import APIRouter

# Build entity imports
from repograph.entities.search.service import SearchService

# Model imports
from repograph.entities.search.models import (
    AvailableSearchQuery,
    SemanticSearchResultSet,
)

# Configure logging
log = getLogger("repograph.entities.search.router")


class SearchRouter:
    service: SearchService
    available_queries: List[AvailableSearchQuery]

    def __init__(self, service: SearchService):
        self.service = service
        self.router = APIRouter(tags=["Search"], prefix="/graph/{graph}/search")
        self.router.add_api_route(
            "/semantic",
            self.semantic_search,
            methods=["GET"],
            response_model=None,
            response_model_exclude={"ast"},
        )
        self.router.add_api_route(
            "/query/available",
            self.available_queries,
            methods=["GET"],
            response_model=List[AvailableSearchQuery],
            response_model_exclude={"function"},
        )
        self.router.add_api_route(
            "/query/{query_id}", self.query_search, methods=["GET"]
        )

        self.graphRouter = APIRouter(tags=["Graph"], prefix="/graph/{graph}")
        self.graphRouter.add_api_route(
            "/incorrect-and-missing-docstrings",
            self.incorrect_docstrings,
            methods=["GET"],
        )

    def semantic_search(
        self, graph: str, query: str = None, offset: int = 0, limit: int = 0
    ) -> SemanticSearchResultSet:
        """Semantic search endpoint."""
        results = self.service.find_similar_functions_by_query(
            graph, query, offset, limit
        )
        return results

    async def incorrect_docstrings(self, graph: str):
        incorrect, missing = self.service.find_possible_incorrect_docstrings(graph)
        return [incorrect, missing]

    async def available_queries(self):
        return self.service.get_available_search_queries()

    async def query_search(self, graph: str, query_id: int):
        query_map = {x.id: x for x in self.service.get_available_search_queries()}

        query = query_map.get(query_id, None)
        if not query:
            raise Exception()  # TODO: Change

        result = query(graph)
        return result
