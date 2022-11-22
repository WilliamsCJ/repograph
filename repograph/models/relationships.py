"""
Relationships between Nodes.
"""
from repograph.models.base import Relationship
from repograph.models.nodes import Argument, Body, Class, Docstring, DocstringArgument, \
                                   DocstringReturnValue, File, Folder, Function, Repository, \
                                   ReturnValue, Package, License


class Requires(Relationship):
    """Requires Relationship.

    Between Repository and (external) Package,
    representing a dependency from a requirements file.

    Attributes:
       version (str): The specific version that is required.
    """
    _allowed_types = {
        Repository: {Package}
    }

    version: str


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


class HasMethod(Relationship):
    """HasMethod Relationship

    Class -> Function
    """
    _allowed_types = {
        Class: {Function}
    }


class HasFunction(Relationship):
    """HasFunction Relationship

    File -> Function
    """
    _allowed_types = {
        File: {Function}
    }


class HasArgument(Relationship):
    """HasArgument Relationship

    Function -> Argument
    """
    _allowed_types = {
        Function: {Argument}
    }


class Returns(Relationship):
    """Returns Relationship

    Function -> ReturnValue
    """
    _allowed_types = {
        Function: {ReturnValue}
    }


class LicensedBy(Relationship):
    """LicensedBy Relationship

    Repository -> License
    """
    _allowed_types = {
        Repository: {License}
    }


class Documents(Relationship):
    """Documents relationship.

    Docstring -> Function
    """
    _allowed_types = {
        Docstring: {Function},
        DocstringArgument: {Argument},
        DocstringReturnValue: {ReturnValue}
    }
