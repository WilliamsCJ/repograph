"""
Routing for build entity.
"""
# pip imports
from fastapi import APIRouter

# Management entity imports


class ManagementRouter:

    def __init__(self, service: BuildService):
        self.service = service
        self.router = APIRouter(prefix="/management")
        self.router.add_api_route("/", self.hello, methods=["GET"])

    def hello(self):
        return {"Hello": "world"}
