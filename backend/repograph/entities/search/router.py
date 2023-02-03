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
        self.router = APIRouter(prefix="/search")
        self.router.add_api_route("/test", self.test, methods=["GET"])

    def test(self):
        self.service.test()
        return {"Hello": "world"}
