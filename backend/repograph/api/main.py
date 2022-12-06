"""
API Main
"""
import logging
import os

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from repograph.repograph import Repograph
from repograph.models.repograph import RepographSummary

log = logging.getLogger('repograph.api')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repograph: Repograph = Repograph(
    os.environ.get("NEO4J_URI"),
    os.environ.get("NEO4J_USER"),
    os.environ.get("NEO4J_PASSWORD"),
    os.environ.get("NEO4J_DATABASE")
)


@app.get(
    "/graph/summary",
    response_model=RepographSummary,
    status_code=status.HTTP_200_OK
)
async def get_summary():
    return repograph.get_summary()
