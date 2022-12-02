"""
Models representing elements of the Repograph
"""

from pydantic import BaseModel


class RepographSummary(BaseModel):
    """
    RepographSummary represents a summary about a Repograph.
    """
    is_empty: bool = True
    classes: int = 0
    functions: int = 0
    modules: int = 0
    packages: int = 0
