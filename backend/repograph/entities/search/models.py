"""
Search entity-related models.
"""
# Base imports
from typing import List

# pip imports
from pydantic import BaseModel, Field, validator

# Model imports
from repograph.entities.graph.models.nodes import Function


class SemanticSearchResult(BaseModel):
    """Result for semantic search query.

    Args:
        function (Function): The function node in the match.
        summarization (str): The summarization of the function's source code.
        score (float): The cosine distance score.
    """
    function: Function = Field(..., exclude={'ast'})
    summarization: str
    score: float

    @validator('score')
    def round_score(cls, v):
        """Round match score to 3 decimal places."""
        return round(v, 3)


class SemanticSearchResultSet(BaseModel):
    results: List[SemanticSearchResult]
    offset: int
    limit: int
    total: int
