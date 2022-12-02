"""
Nodes.
"""
from enum import Enum
from typing import Any, Optional

from repograph.models.base import Node
from repograph.utils.paths import get_path_name, get_path_parent, get_package_parent_and_name


class Repository(Node):
    """Represents a software repository.

    Attributes:
        name: The name of the repository.
        type: The inferred repository type.
    """
    name: str
    type: str  # TODO: Is this correct? Invocation?


class Directory(Node):
    """Represents a folder in a repository.

    Attributes:
        name (str): The name of the directory.
        path (str): The path of the directory.
        parent (str): The parent directory of the folder.
    """
    name: str
    path: Optional[str]
    parent_path: Optional[str]

    def __init__(self, path=None):
        """_summary_

        Args:
            path (_type_): _description_
        """
        name = get_path_name(path)
        parent = get_path_parent(path)
        super().__init__(path=path, name=name, parent=parent)


class Package(Directory):
    """Represents a Python package, either within the repository or external.

     Attributes:
        canonical_name (str): The full package name.
        parent_package (str): The canonical name of the parent package.
        external (bool): Whether this package is external to the parent repository
                         (i.e. installed from PyPi).
    """
    canonical_name: str
    parent_package: str
    external: bool

    @classmethod
    def create_from_directory(cls, path: str, canonical_name: str) -> "Package":
        parent, name = get_package_parent_and_name(canonical_name)
        return Package(
            name,
            canonical_name,
            parent,
            path=path,
            parent_path=get_path_parent(path),
            parent_package=parent,
        )

    @classmethod
    def create_from_external_dependency(cls, package: str) -> "Package":
        """Creates a Package instance from an external dependency.

        Args:
            package (str): The dependency name.

        Returns:
            Package: A Package instance.
        """
        parent, name = get_package_parent_and_name(package)
        return Package(
            name,
            package,
            parent,
            external=True
        )

    def __init__(
        self,
        name: str,
        canonical_name: str,
        parent_package: str,
        path: Optional[str] = None,
        parent_path: Optional[str] = None,
        external: bool = False
    ):
        """Constructor

        Args:
            name (str): The name of the package.
            canonical_name (str): The full canonical name (including all parents) of the package.
            parent_package (str): The canonical name of the
            path (Optional[str], optional): The path of the package. Defaults to None.
            parent_path (Optional[str], optional): The path of the parent package. Defaults to None.
            external (bool, optional): Whether the package is an external dependency of
                                       the repository. Defaults to False.
        """
        super(Directory, self).__init__(
            name=name,
            canonical_name=canonical_name,
            parent_package=parent_package,
            path=path,
            parent_path=parent_path,
            external=external
        )


class Module(Node):
    """Represents a Module within the repository.

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
        min_line_number (Optional[int]): The first line of the class definition.
        max_line_number (Optional[int): The last line of the class definition.
    """
    name: str
    min_line_number: Optional[int]
    max_line_number: Optional[int]


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
    name: Optional[str]
    type: Optional[str] = "Any"


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


class Docstring(Node):
    """Represents a docstring for a function or class.

    Attributes:
        short_description (str): The short headline description of the docstring.
        long_description (Optional[str]): The main body of the docstring.
        summarization (str): The generated text summary of whatever the docstring is documenting.
    """
    short_description: str
    long_description: Optional[str]
    summarization: Optional[str]


class DocstringArgument(Argument):
    """Represents an argument description with a docstring.

    Attributes:
        name (str): The argument name.
        description (str): The description of the argument.
        type (str): The inferred type of the variable, usually from a type hint.
        is_optional (bool): Whether the argument is optional.
        default (Optional[Any]): The default value of the argument, if it is optional.
    """
    description: Optional[str]
    is_optional: bool
    default: Optional[Any]


class DocstringReturnValue(ReturnValue):
    """Represents a return value description within a docstring.

    Attributes:
        name (str): The argument name.
        description (str): The description of the argument.
        type (str): The inferred type of the variable, usually from a type hint.
        is_generator (bool): Whether the return value is a generator.
    """
    description: Optional[str]
    is_generator: bool


class DocstringRaises(Node):
    """Represents a raises/exception descritpion within a docstring.

    Args:
        description (str): The description of the exception that may be raised.
        type (str): The inferred type of the exception, usually from a type hint.
    """
    description: str
    type: Optional[str]
