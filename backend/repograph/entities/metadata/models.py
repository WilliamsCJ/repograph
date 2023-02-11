"""
Data models for the Metadata entity.
"""
# Base imports
import datetime

# pip imports
from pydantic import BaseModel, Field


class Graph(BaseModel):
    """
    Represents a Graph within Neo4j.
    """
    neo4j_name: str
    name: str
    description: str
    created: datetime.datetime = Field(default_factor=datetime.datetime.now)
