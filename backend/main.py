"""
API Main
"""
import os

from fastapi import FastAPI

from backend.repograph.repograph import Repograph

app = FastAPI()

repograph: Repograph = Repograph(
    os.environ.get("NEO4J_URI"),
    os.environ.get("NEO4J_USER"),
    os.environ.get("NEO4J_PASSWORD"),
    os.environ.get("NEO4J_DATABASE")
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
