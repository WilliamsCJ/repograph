# pragma: no cover
# TODO: Maybe some unit tests?
"""
Routing for build entity.
"""
# Base imports
from logging import getLogger
from typing import List

# pip imports
from fastapi import APIRouter

from repograph.entities.graph.models.graph import IssuesResult
# Build entity imports
from repograph.entities.search.service import SearchService

# Model imports
from repograph.entities.search.models import (
    AvailableSearchQuery,
    SemanticSearchResultSet,
)
from repograph.utils.exception_handlers import RepographException

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
            "/incorrect-docstrings",
            self.incorrect_docstrings,
            methods=["GET"],
        )
        self.graphRouter.add_api_route(
            "/missing-docstrings",
            self.missing_docstrings,
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
        incorrect = self.service.find_incorrect_docstrings(graph)
        return IssuesResult(
            columns=["Name", "Type", "Summarization", "Docstring", "Similarity", "Repository"],
            data=incorrect
        )

    async def missing_docstrings(self, graph: str):
        missing = self.service.find_missing_docstrings(graph)
        return IssuesResult(
            columns=["Name", "Type", "Repository"],
            data=missing
        )

    async def available_queries(self):
        return self.service.get_available_search_queries()

    async def query_search(self, graph: str, query_id: int, repository: str = None):
        query_map = {x.id: x for x in self.service.get_available_search_queries()}

        query = query_map.get(query_id, None)
        if not query:
            raise RepographException

        result = query.function(graph, repository=repository)
        return result
