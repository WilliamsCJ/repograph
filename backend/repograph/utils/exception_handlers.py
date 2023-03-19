"""Custom exception handlers.
This module provides custom exception handlers that are triggered when exceptions are raised
to the router handlers.
"""
# pip imports
from fastapi import status
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


class RepographException(Exception):
    """
    Custom base exception.
    """

    message: str = "An error occurred."
    code: status = status.HTTP_500_INTERNAL_SERVER_ERROR


async def base_exception_handler(_: Request, e: RepographException):
    """Generic exception handler.
    This handler is for all other Exceptions, to provide a formatted response.
    Args:
        _ (Request): FastAPI request object. Not used.
        e (RepographException): The RepographException object.
    Returns:
        JSONResponse containing ErrorResponse.
    """
    return JSONResponse(ErrorResponse(message=e.message).dict(), status_code=e.code)  # pragma: no cover


async def generic_exception_handler(_: Request, __: Exception):
    """Generic exception handler.
    This handler is for all other Exceptions, to provide a formatted response.
    Args:
        _ (Request): FastAPI request object. Not used.
        __ (Exception): The Exception object.
    Returns:
        JSONResponse containing ErrorResponse.
    """
    return JSONResponse(  # pragma: no cover
        ErrorResponse(message="Internal Server Error").dict(), status_code=500
    )
