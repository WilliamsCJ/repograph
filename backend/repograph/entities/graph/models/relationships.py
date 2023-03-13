"""
Relationships between Nodes.
"""
from typing import List, Optional, Tuple

from repograph.entities.graph.models.base import Relationship
from repograph.entities.graph.models.nodes import (
    Argument,
    Body,
    Class,
    Docstring,
    DocstringArgument,
    DocstringRaises,
    DocstringReturnValue,
    Module,
    Directory,
    Function,
    README,
    Repository,
    ReturnValue,
    Package,
    License,
    Variable,
)


class Requires(Relationship):
    """Requires Relationship.

    Between Repository and (external) Package,
    representing a dependency from a requirements file.

    Attributes:
       version (str): The specific version that is required.
    """

    _allowed_types = {Repository: {Package}}

    specifications: List[str]


class Contains(Relationship):
    """Contains Relationship

    Usage:
      - Folder -> Folder/Module
      - Module -> Class/Function, Body
    """

    _allowed_types = {
        Repository: {Directory, Module, Package, README},
        Directory: {Directory, Module, Package, README},
        Package: {Directory, Module, Package, README},
        Module: {Function, Class, Body, Variable},
    }


class Imports(Relationship):
    """Imports Relationship

    Usage:
        - Module -> Module, Function, Package, Class
    """

    _allowed_types = {
        Module: {Module, Package, Class, Function, Variable},
    }

    alias: Optional[str]


class HasMethod(Relationship):
    """HasMethod Relationship

    Class -> Function
    """

    _allowed_types = {Class: {Function}}


class Extends(Relationship):
    """Extends Relationship

    Class -> Class
    """

    _allowed_types = {Class: {Class}}


class HasFunction(Relationship):
    """HasFunction Relationship

    Module -> Function
    """

    _allowed_types = {Module: {Function}}


class HasArgument(Relationship):
    """HasArgument Relationship

    Function -> Argument
    """

    _allowed_types = {Function: {Argument}}


class Returns(Relationship):
    """Returns Relationship

    Function -> ReturnValue
    """

    _allowed_types = {Function: {ReturnValue}}


class LicensedBy(Relationship):
    """LicensedBy Relationship

    Repository -> License
    """

    _allowed_types = {Repository: {License}}


class Documents(Relationship):
    """Documents relationship.

    Docstring -> Function
    """

    _allowed_types = {
        Docstring: {Function, Class},
    }


class Describes(Relationship):
    """Describes relationship.

    Docstring -> DocstringArgument OR DocstringReturnValue
    """

    _allowed_types = {
        Docstring: {DocstringArgument, DocstringRaises, DocstringReturnValue}
    }


class Calls(Relationship):
    """Calls relationship.

    Module -> Function, Class
    Function -> Function, Class
    """

    _allowed_types = {Module: {Function, Class}, Function: {Function, Class, Module}}
