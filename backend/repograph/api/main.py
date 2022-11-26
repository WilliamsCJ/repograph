"""
API Main
"""
import os

from fastapi import FastAPI, status

from repograph.repograph import Repograph
from repograph.models.repograph import RepographSummary

app = FastAPI()

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
