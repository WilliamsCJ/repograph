"""
Custom exceptions for the graph entity.
"""
# pip imports
from fastapi import status


# Exceptions imports
from repograph.utils.exception_handlers import RepographException


class InvalidGraphNameError(RepographException):
    """
    Exception for invalid graph names.
    """

    code = status.HTTP_406_NOT_ACCEPTABLE

    def __init__(self, graph_name: str):
        self.message = f"The graph name '{graph_name}' is invalid!"


class GraphExistsError(RepographException):
    """
    Exception for invalid
    """

    code = status.HTTP_409_CONFLICT

    def __init__(self, graph_name: str):
        self.message = f"The graph '{graph_name}' already exists!"
