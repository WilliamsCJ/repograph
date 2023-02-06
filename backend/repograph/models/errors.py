"""
Models related to error-handling.
"""
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Generic error response.

    Attributes:
        status (str): Always "error"
        message (str): Message describe error. Should match status code.
    """
    status: str = "ERROR"
    message: str
