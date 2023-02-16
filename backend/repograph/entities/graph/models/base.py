"""
"""
from __future__ import annotations
import py2neo
from pydantic import BaseModel, PrivateAttr
from typing import Any, Dict, Optional, Set, Union


class BaseSubgraph(BaseModel):
    """Base Subgraph is the base class for Nodes and Relationships.

    As with Py2neo's Subgraph, BaseSubgraph is the superclass for Nodes
    and Relationships that compose a Graph.

    Subclass of Pydantic's BaseModel for attribute verification, etc.

    The actual Py2Neo Subgraph is stored as a private attribute,
    as multiple inheritance not possible due to layout conflict.
    https://github.com/pydantic/pydantic/issues/3523s

    Attributes:
        _subgraph (py2neo.Subgraph): Py2neo Node representation.
    """

    _subgraph: py2neo.Subgraph = PrivateAttr()
    id: Optional[int]
    repository_name: str

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        subgraph: Union[py2neo.Node, py2neo.Relationship],
        repository_name: str,
        identity: Optional[int] = None,
        **data: Any,
    ) -> None:
        """Constructor

        Args:
            subgraph (py2neo.Subgraph): Subgraph - either Node or Relationship.
            repository_name (str): The name of the repository this node is connected to.
            identity (int, optional): Optional entity ID.
        """
        self._subgraph = subgraph

        super().__init__(id=identity, repository_name=repository_name, **data)


class Node(BaseSubgraph):
    """Node represents a generic Node in Repograph.

    All Node types inherit from this class.
    """

    def __init__(
        self, repository_name: str = None, identity: Optional[int] = None, **data: Any
    ) -> None:
        """Constructor

        Args:
            **data (Any): Attribute kwargs

        Calls BaseSubgraph superclass constructor, and
        also creates the internal _subgraph attribute,
        specifically with a Node object.

        Class name used as Py2neo Node label.
        """
        super().__init__(
            py2neo.Node(
                self.__class__.__name__, repository_name=repository_name, **data
            ),
            repository_name,
            identity=identity,
            **data,
        )


class InvalidRelationshipException(TypeError):
    """Represent an invalid Relationship configuration,
    based on the parent and child types.
    """

    def __init__(self, parent: Node, child: Node, relationship: Relationship) -> None:
        """Constructor

        Args:
            parent (Node): Parent node.
            child (Node): Child node.
            relationship (Relationship): The attempted relationship.
        """
        message = f"""
          {type(parent)} -> {type(child)} is not a valid
          pairing for relationship of type: {type(Relationship)}
          """
        super().__init__(message)


class Relationship(BaseSubgraph):
    """Relationship represents a generic Relationship in Repograph.

    All Relationships types inherit from this class.

    Args:
        parent (Node): The parent Node.
        child (Node): The child Node.

    Raises:
        InvalidRelationshipException: _description_
    """

    parent: Node
    child: Node

    _allowed_types: Optional[Dict[Node, Set[Node]]] = None

    def __init__(
        self, parent: Node, child: Node, repository_name: str, **data: Any
    ) -> None:
        """Constructor

        Args:
            parent (Node): The parent Node.
            child (Node): The child Node.

        Raises:
            InvalidRelationshipException: If the types of the parent and child Nodes violate
                                          the mappings in _allowed_types.
        """
        if self._allowed_types and (
            type(child) not in self._allowed_types.get(type(parent), set())
        ):  # noqa: E501
            raise InvalidRelationshipException(parent, child, self)

        super().__init__(
            py2neo.Relationship(
                parent._subgraph,
                self.__class__.__name__,
                child._subgraph,
                repository_name=repository_name,
                **data,
            ),
            repository_name,
            parent=parent,
            child=child,
            **data,
        )
