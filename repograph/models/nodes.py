import abc
from enum import Enum
from py2neo import Node
from typing import Any, List

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
    """Node representing file in a repository.

    Extends NodeABC.

    Attributes:
       name (str): The file.
       path (str): The file path within the repository.
       extension (str): The file extension.
       is_test (bool): Whether the file has been assessed to be a test file.
    """
    name: str
    path: str
    extension: str
    is_test: bool

    def __init__(self, name, path, extension, is_test) -> None:
        self.path = path
        self.name = name
        self.extension = extension
        self.is_test = is_test
        super().__init__(name=name, path=path, extension=extension, is_test=is_test)


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
    """Node representing a Python function, including methods.

    Extends NodeABC.

    Attributes:
        name (str): The name of the function or method.
        type (FunctionType): Whether this is a function or a method.
        source_code (str): The original source code string.
        ast (ast.AST): Abstract Syntax Tree extracted from the source code.
        min_line_number (int): The first line of the function definition.
        max_line_number (int): The last line of the function definition.
    """
    class FunctionType(Enum):
        """Enum for FunctionType.

        Either Method or Function.
        """
        METHOD = "Method"
        FUNCTION = "Function"

    name: str
    type: FunctionType
    source_code: str
    ast: Any
    min_line_number: int
    max_line_number: int

    def __init__(
        self,
        name: str,
        type: FunctionType,
        source_code: str,
        ast: Any,
        min_line_number: int,
        max_line_number: int
    ) -> None:
        """Function constructor.

        Args:
            name (str): The name of the function or method.
            type (FunctionType): Whether this is a function or a method.
            source_code (str): The original source code string.
            ast (ast.AST): Abstract Syntax Tree extracted from the source code.
        """
        self.name = name
        self.type = type
        self.source_code = source_code
        self.ast = ast
        self.min_line_number = min_line_number
        self.max_line_number = max_line_number

        super().__init__(
            name=name,
            type=type,
            source_code=source_code,
            ast=ast,
            min_line_number=min_line_number,
            max_line_number=min_line_number,
        )


class Variable(NodeABC):
    name: str
    type: str

    def __init__(self, name: str, type: str = "Any") -> None:
        """Constructor

        Args:
            name (str): The variable name.
            type (str, optional): The type of the variable. Defaults to "Any".
        """
        self.name = name
        self.type = type
        super().__init__(name=name, type=type)


class Argument(Variable):
    """Node representing an argument to a function.

    Extends Variable
    """


class ReturnValue(Variable):
    """Node representing a return value from a function.

    Extends Variable.
    """


class Body(NodeABC):
    pass
