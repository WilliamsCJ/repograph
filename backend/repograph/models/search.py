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
    function: Function = Field(..., exclude={'ast'})
    summarization: str
    score: float

    @validator('score')
    def result_check(cls, v):
        return round(v, 3)
