"""
Search entity-related models.
"""
# pip imports
from pydantic import BaseModel, Field, validator

# Model imports
from repograph.models.nodes import Function


class SemanticSearchResult(BaseModel):
    """Result for semantic search query.

    Args:
        function (Function): The function node in the match.
        summarization (str): The summarization of the function's source code.
        score (float): The cosine distance score.
    """
    id: int
    function: Function = Field(..., exclude={'ast'})
    summarization: str
    score: float

    @validator('score')
    def round_score(cls, v):
        """Round match score to 3 decimal places."""
        return round(v, 3)
