"""
Routing for build entity.
"""
# pip imports
from fastapi import APIRouter

# Build entity imports
from repograph.entities.search.service import SearchService


class SearchRouter:
    service: SearchService

    def __init__(self, service: SearchService):
        self.service = service
        self.router = APIRouter(tags=["Search"], prefix="/graph/{graph}/search")
        self.router.add_api_route(
            "/semantic",
            self.semantic_search,
            methods=["GET"],
            response_model_exclude={"ast"}
        )

    def semantic_search(self, graph: str, query: str = None):
        results = self.service.find_similar_functions_by_query(query)
        print(results[0].function._subgraph._identity)
        return results
