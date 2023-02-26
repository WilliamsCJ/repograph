# pragma: no cover
"""
Routing for metadata entity.
"""
# pip imports
from fastapi import APIRouter, status

# Graph entity imports
from repograph.entities.metadata.service import MetadataService


class MetadataRouter:
    service: MetadataService

    def __init__(self, service: MetadataService):
        self.service = service

        self.router = APIRouter(prefix="/metadata", tags=["Summary"], responses={})

        self.router.add_api_route(
            "/graphs", self.get_all, methods=["GET"], status_code=status.HTTP_200_OK
        )

    async def get_all(self):
        return self.service.get_all_graph_listings()
