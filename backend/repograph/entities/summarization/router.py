"""
Routing for build entity.
"""
# pip imports
from fastapi import APIRouter

# Build entity imports
from repograph.entities.build.service import BuildService


class BuildRouter:
    service: BuildService

    def __init__(self, service: BuildService):
        self.service = service
        self.router = APIRouter(prefix="/summarization")
        self.router.add_api_route("/", self.hello, methods=["GET"])

    def hello(self):
        return {"Hello": "world"}
