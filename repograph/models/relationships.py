import abc
from py2neo import Node, Relationship
from typing import Dict, Set, Union

from repograph.models.nodes import Argument, Body, Class, File, Folder, Function, \
                                   NodeABC, Repository, ReturnValue


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

    def __init__(self, parent: Class, child: Function, **kwargs) -> None:
        super().__init__(parent, child, **kwargs)


class HasFunction(Relationship):
    _allowed_types = {
        File: {Function}
    }

    def __init__(self, parent: Class, child: Function, **kwargs) -> None:
        super().__init__(parent, child, **kwargs)


class HasArgument(Relationship):
    def __init__(self, parent: Function, child: Argument) -> None:
        super().__init__(parent, child)


class Returns(Relationship):
    def __init__(self, parent: Function, child: ReturnValue) -> None:
        super().__init__(parent, child)


class Calls(Relationship):
    """
    Represents the Calls relationship between TODO: Finish
    """
    def __init__(self, parent: NodeABC, child: Node) -> None:
        """Calls constructor.

        Args:
            parent (NodeABC): TODO: Make this more precise
            child (Node): The Node being called
        """
        super().__init__(parent, child)
