# pragma: no cover
# TODO: Maybe some unit tests?
"""
Routing for build entity.
"""
# Base imports
from io import BytesIO
import os
import shutil
from zipfile import ZipFile
from uuid import uuid4
from typing import List

# pip imports
from fastapi import APIRouter, BackgroundTasks, Form, UploadFile

# Build entity imports
from repograph.entities.build.service import BuildService

# Utils imports
from repograph.utils.exception_handlers import RepographException


class BuildRouter:
    service: BuildService

    def __init__(self, service: BuildService):
        self.service = service
        self.router = APIRouter(prefix="/graph")
        self.router.add_api_route("/build", self.build, methods=["POST"])

    def _cleanup_inputs(self, inputs: List[str]):
        for p in inputs:
            shutil.rmtree(p, ignore_errors=True)

    def build(
        self,
        files: list[UploadFile],
        background_tasks: BackgroundTasks,
        name: str = Form(),
        description: str = Form(),
    ):
        paths = []
        cleanup_inputs = []

        try:
            for file in files:
                with ZipFile(BytesIO(file.file.read()), "r") as repository:
                    u = str(uuid4())
                    outer_path = str(os.path.join(os.getcwd(), u))
                    repository.extractall(path=outer_path)

                    if len(os.listdir(outer_path)) == 1:
                        paths.append(
                            str(os.path.join(outer_path, os.listdir(outer_path)[0]))
                        )
                    else:
                        paths.append(outer_path)

                    cleanup_inputs.append(outer_path)
        except RepographException as e:
            background_tasks.add_task(self._cleanup_inputs, cleanup_inputs)
            raise e

        background_tasks.add_task(
            self.service.build,
            paths,
            name,
            description,
        )

        background_tasks.add_task(self._cleanup_inputs, cleanup_inputs)

        return {"status": "pending"}
