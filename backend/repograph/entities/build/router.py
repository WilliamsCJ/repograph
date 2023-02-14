"""
Routing for build entity.
"""
# Base imports
from io import BytesIO
import os
from zipfile import ZipFile
from uuid import uuid4

# pip imports
from fastapi import APIRouter, BackgroundTasks, Form, UploadFile

# Build entity imports
from repograph.entities.build.service import BuildService


class BuildRouter:
    service: BuildService

    def __init__(self, service: BuildService):
        self.service = service
        self.router = APIRouter(prefix="/graph")
        self.router.add_api_route("/build", self.build, methods=["POST"])

    def build(
        self,
        files: list[UploadFile],
        background_tasks: BackgroundTasks,
        name: str = Form(),
        description: str = Form(),
    ):
        paths = []

        for file in files:
            with ZipFile(BytesIO(file.file.read()), "r") as repository:
                u = str(uuid4())
                outer_path = str(os.path.join(os.getcwd(), u))
                repository.extractall(path=outer_path)

                if len(os.listdir(outer_path)) == 1:
                    paths.append(str(os.path.join(outer_path, os.listdir(outer_path)[0])))
                else:
                    paths.append(outer_path)

        background_tasks.add_task(
            self.service.build,
            paths,
            name,
            description,
            cleanup_inputs=True
        )

        return {"status": "pending"}
