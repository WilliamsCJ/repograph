"""
Routing for build entity.
"""
# Base imports
from logging import getLogger

# pip imports
from fastapi import APIRouter

# Build entity imports
from repograph.entities.search.service import SearchService

# Model imports
from repograph.entities.search.models import SemanticSearchResultSet

# Configure logging
log = getLogger("repograph.entities.search.router")


class SearchRouter:
    service: SearchService

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
