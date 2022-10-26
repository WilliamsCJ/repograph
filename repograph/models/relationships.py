import abc
from py2neo import Node, Relationship
from typing import Dict, Set, Union

from repograph.models.nodes import Argument, Body, Class, File, Folder, Function, \
                                   NodeABC, Repository


class RelationshipABC(abc.ABC, Relationship):
    """Abstract Base Class for Relationships.

    Extends the Relationship class from py2neo
    """
    _allowed_types: Dict[Node, Set[Node]]

    def __init__(self, parent, child, **kwargs) -> "RelationshipABC":
        """RelationshipABC constructor.

        Args:
          **kwargs: Keyword arguments

        Returns:
          RelationshipABC: An instance of a RelationshipABC subclass.
        """
        allowed_types = self._allowed_types(type(parent))

        if not allowed_types or type(child) not in allowed_types:
            raise InvalidRelationshipException(parent, child, self.__class__.__name)

        Relationship.__init__(parent, self.__class__.__name, child, **kwargs)


class InvalidRelationshipException(TypeError):
    def __init__(self, parent: NodeABC, child: NodeABC, relationship: str) -> None:
        message = f"""
          {type(parent)} -> {type(child)} is not a valid
          pairing for relationship of type: {relationship}
          """
        super().__init__(message)


class Contains(Relationship):
    """Contains Relationship

    Usage:
      - Folder -> Folder/File
      - File -> Class/Function, Body
    """
    _allowed_types = {
      Repository: {Folder, File},
      Folder: {Folder, File},
      File: {Function, Class, Body}
    }

    def __init__(
        self,
        parent: Union[File, Folder, Repository],
        child: Union[Body, Class, File, Folder, Function]
    ) -> None:
        super().__init__(parent, child)


class HasMethod(Relationship):
    _allowed_types = {
        Class: {Function}
    }

    def __init__(self, parent: Class, child: Function, **kwargs) -> RelationshipABC:
        super().__init__(parent, child, **kwargs)


class HasArgument(Relationship):
    _allowed_types = {
        Function: {Argument}
    }

    def __init__(self, parent: Function, child: Argument) -> RelationshipABC:
        super().__init__(parent, child)
