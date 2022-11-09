"""
Nodes.
"""
from enum import Enum
from typing import Any, List

from repograph.models.base import Node
import repograph.utils as utils


class Repository(Node):
    """Represents a software repository.

    Attributes:
        name: The name of the repository.
        type: The inferred repository type.
    """
    name: str
    type: str  # TODO: Is this correct? Invocation?


class Package(Node):
    """Represents a Python package.

    Attributes:
        name (str): The name of the package
        external (bool): Whether this package is external to the parent repository
                         (i.e. installed from PyPi).
    """
    name: str
    external: bool


class Folder(Node):
    """Represents a folder in a repository.

    Attributes:
        name (str): The name of the folder.
        path (str): The path of the folder.
        parent (str): The parent directory of the folder.
    """
    name: str
    path: str
    parent: str

    def __init__(self, path):
        """_summary_

        Args:
            path (_type_): _description_
        """
        name = utils.get_path_name(path)
        parent = utils.get_path_parent(path)
        super().__init__(path=path, name=name, parent=parent)


class File(Node):
    """Represents a File within the repository.

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


class Class(Node):
    """Represents a Python class.

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


class Function(Node):
    """Represents a Python function or method.

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


class Variable(Node):
    """Represents a Python variable.

    Attributes:
        name (str): The variable name
        type (str): The inferred type of the variable, usually from a type hint.
    """
    name: str
    type: str = "Any"


class Argument(Variable):
    """Node representing an argument to a function.
    """


class ReturnValue(Variable):
    """Node representing a return value from a function.
    """


class Body(Node):
    pass


class License(Node):
    """Represents a software license.
    Defines the licensing terms of a repository.

    Attributes:
        text (str): The raw text of the license.
        license_type (str): The suspected license type.
        confidence (float): The confidence that the specified type matches the extracted text.
    """
    text: str
    license_type: str
    confidence: float
