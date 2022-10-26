import abc
import ast
from py2neo import Node
from typing import List

import repograph.utils as utils


class NodeABC(abc.ABC, Node):
    def __init__(self, **kwargs) -> None:
        super().__init__(self.__class__.__name__, **kwargs)


class Folder(NodeABC):
    name: str
    path: str
    parent: str

    def __init__(self, path):
        self.path = path
        self.name = utils.get_path_name(path)
        self.parent = utils.get_path_parent(path)
        super().__init__(path=self.path, name=self.name, parent=self.parent)


class Repository(NodeABC):
    name: str
    type: str

    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type
        super().__init__(name=name, type=type)


class File(NodeABC):
    name: str
    path: str
    extension: str

    def __init__(self, name, path, extension) -> None:
        self.path = path
        self.name = name
        self.extension = extension
        super().__init__(name=name, path=path, extension=extension)


class Class(NodeABC):
    """Node representing a Python class.

    Extends NodeABC.

    Attributes:
        name (str): The class name.
        min_line_number (int): The first line of the class definition.
        max_line_number (int): The last line of the class definition.
        extends (List[str]): A list of other classes/types that the class extends.
    """
    name: str
    min_line_number: int
    max_line_number: int
    extends: List[str]

    def __init__(
        self,
        name: str,
        min_line_number: int,
        max_line_number: int,
        extends: List[str]
    ) -> None:
        """Class constructor.

        Args:
            name (str): The class name.
            min_line_number (int): The first line of the class definition.
            max_line_number (int): The last line of the class definition.
            extends (List[str]): A list of other classes/types that the class extends.
        """
        self.name = name
        self.min_line_number = min_line_number
        self.max_line_number = max_line_number
        self.extends = extends
        super().__init__(
            name=name,
            min_line_number=min_line_number,
            max_line_number=max_line_number,
            extends=extends
        )


class Function(NodeABC):
    name: str
    source_code: str
    ast: ast.AST


class Body(NodeABC):
    pass
