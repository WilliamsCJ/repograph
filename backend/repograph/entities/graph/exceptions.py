"""
Custom exceptions for the graph entity.
"""
# pip imports
from fastapi import status


# Exceptions imports
from repograph.utils.exception_handlers import RepographException


class GraphExistsError(RepographException):
    code = status.HTTP_409_CONFLICT

    def __init__(self, graph_name: str):
        self.message = f"The graph '{graph_name}' already exists!"
