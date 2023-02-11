"""Custom exception handlers.
This module provides custom exception handlers that are triggered when exceptions are raised
to the router handlers.
"""
# pip imports
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Generic error response.

    Attributes:
        status (str): Always "error"
        message (str): Message describe error. Should match status code.
    """
    status: str = "ERROR"
    message: str


async def generic_exception_handler(_: Request, __: Exception):
    """Generic exception handler.
    This handler is for all other Exceptions, to provide a formatted response.
    Args:
        _ (Request): FastAPI request object. Not used.
        __ (Exception): The Exception object.
    Returns:
        JSONResponse containing ErrorResponse.
    """
    return JSONResponse(
        ErrorResponse(message="Internal Server Error").dict(),
        status_code=500
    )
