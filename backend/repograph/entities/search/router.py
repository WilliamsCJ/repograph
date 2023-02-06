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
from repograph.models.search import SemanticSearchResultSet

# Configure logging
log = getLogger('repograph.entities.search.router')


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

    def semantic_search(
            self,
            graph: str,
            query: str = None,
            offset: int = 0,
            limit: int = 0
    ) -> SemanticSearchResultSet:
        """Semantic search endpoint."""
        results = self.service.find_similar_functions_by_query(query, offset, limit)
        return results
