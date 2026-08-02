"""
Nodes.
"""

import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import Field

from repograph.entities.graph.models.base import Node
from repograph.utils import JSONDict
from repograph.entities.graph.utils import (
    get_path_name,
    get_path_parent,
    get_package_parent_and_name,
)

PYTHON_EXTENSION = ".py"


class Repository(Node):
    """Represents a software repository.

    Attributes:
        name: The name of the repository.
        type: The inferred repository type.
    """

    class SoftwareType(Enum):
        """Enum for SoftwareType of Repository."""

        SERVICE = "service"
        SCRIPT_WITH_MAIN = "script with main"
        SCRIPT_WITHOUT_MAIN = "script without main"
        SCRIPT = "script"
        PACKAGE = "package"
        LIBRARY = "library"

    # Core
    name: str
    full_name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[SoftwareType] = None
    homepage: Optional[str] = None
    html_url: Optional[str] = None
    url: Optional[str] = None
    default_branch: Optional[str] = None
    visibility: Optional[str] = None
    language: Optional[str] = None
    # Timestamps
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    pushed_at: Optional[datetime.datetime] = None
    # Metrics
    size: Optional[int] = None
    stargazers_count: Optional[int] = None
    watchers_count: Optional[int] = None
    forks_count: Optional[int] = None
    open_issues_count: Optional[int] = None
    forks: Optional[int] = None
    open_issues: Optional[int] = None
    watchers: Optional[int] = None
    network_count: Optional[int] = None
    subscribers_count: Optional[int] = None
    # Flags
    is_root_package: bool
    private: Optional[bool] = None
    fork: Optional[bool] = None
    has_issues: Optional[bool] = None
    has_projects: Optional[bool] = None
    has_downloads: Optional[bool] = None
    has_wiki: Optional[bool] = None
    has_pages: Optional[bool] = None
    has_discussions: Optional[bool] = None
    archived: Optional[bool] = None
    disabled: Optional[bool] = None
    allows_forking: Optional[bool] = None
    is_template: Optional[bool] = None
    web_commit_signoff_required: Optional[bool] = None
    # URLs
    forks_url: Optional[str] = None
    keys_url: Optional[str] = None
    collaborators_url: Optional[str] = None
    teams_url: Optional[str] = None
    hooks_url: Optional[str] = None
    issue_events_url: Optional[str] = None
    events_url: Optional[str] = None
    assignees_url: Optional[str] = None
    branches_url: Optional[str] = None
    tags_url: Optional[str] = None
    blobs_url: Optional[str] = None
    git_tags_url: Optional[str] = None
    git_refs_url: Optional[str] = None
    trees_url: Optional[str] = None
    statuses_url: Optional[str] = None
    languages_url: Optional[str] = None
    stargazers_url: Optional[str] = None
    contributors_url: Optional[str] = None
    subscribers_url: Optional[str] = None
    subscription_url: Optional[str] = None
    commits_url: Optional[str] = None
    git_commits_url: Optional[str] = None
    comments_url: Optional[str] = None
    issue_comment_url: Optional[str] = None
    contents_url: Optional[str] = None
    compare_url: Optional[str] = None
    merges_url: Optional[str] = None
    archive_url: Optional[str] = None
    downloads_url: Optional[str] = None
    issues_url: Optional[str] = None
    pulls_url: Optional[str] = None
    milestones_url: Optional[str] = None
    notifications_url: Optional[str] = None
    labels_url: Optional[str] = None
    releases_url: Optional[str] = None
    deployments_url: Optional[str] = None
    git_url: Optional[str] = None
    ssh_url: Optional[str] = None
    clone_url: Optional[str] = None
    svn_url: Optional[str] = None

    @classmethod
    def create_from_metadata(
        cls,
        name: str,
        metadata: JSONDict,
        is_root_package: bool,
        software_type: Optional[SoftwareType],
        repository_name: str,
    ) -> "Repository":
        """Create from metadata JSON.

        Args:
            name (str): Fallback name for the repository.
            metadata (JSONDict): The metadata JSONDict.
            is_root_package (bool): Whether the repository root is a package.
            software_type (SoftwareType): The extracted software type

        Returns:
            Repository
        """
        metadata.pop("owner", None)
        metadata.pop("license", None)
        metadata.pop("topics", None)
        metadata.pop("organization", None)
        metadata.pop("name", None)
        metadata.pop("id", None)

        return Repository(
            name=name,
            is_root_package=is_root_package,
            type=software_type,
            repository_name=repository_name,
            **metadata,
        )


class README(Node):
    """Represents a README file in a repository.

    Attributes:
        path (str): The path of the README file.
        content (str): The content of the README file.
    """

    path: str
    content: str


class Directory(Node):
    """Represents a folder in a repository.

    Attributes:
        name (str): The name of the directory.
        path (str): The path of the directory.
        parent_path (str): The parent directory of the folder.
        inferred (bool): Whether this directory has been inferred when walking paths provided by
                         inspect4py
    """

    name: str
    path: str
    parent_path: str
    inferred: bool = False

    def __init__(self, path: str, repository_name: str, inferred: bool = False):
        """Create directory

        Args:
            repository_name (str): Repository name
            path (str): Path of directory
            inferred (bool): Whether this directory has been inferred when walking paths provided by
                         inspect4py
        """
        name = get_path_name(path)
        parent = get_path_parent(path)
        super().__init__(
            path=path,
            name=name,
            parent_path=parent,
            repository_name=repository_name,
            inferred=inferred,
        )


class Package(Node):
    """Represents a Python package, either within the repository or external.

    Attributes:
        name (str): The name of the directory.
        path (Optional[str]): The path of the directory.
        parent_path (Optional[str]): The parent directory of the folder.
        canonical_name (str): The full package name.
        parent_package (str): The canonical name of the parent package.
        external (bool): Whether this package is external to the parent repository
                         (i.e. installed from PyPi).
        inferred (bool): This object was inferred when parsing dependencies or calls. Default False.
    """

    name: str
    canonical_name: str
    parent_package: str
    path: Optional[str] = None
    parent_path: Optional[str] = None
    external: bool
    inferred: bool = False

    @classmethod
    def create_from_directory(
        cls,
        path: str,
        canonical_name: str,
        repository_name: str,
    ) -> "Package":
        """Creates a Package instance from a directory.

        Args:
            path (str): The dependency name.
            canonical_name (str): The canonical name of the package.
            repository_name (str): The name of the associated repository.

        Returns:
            Package: A Package instance.
        """
        parent, name = get_package_parent_and_name(canonical_name)
        return Package(
            name,
            canonical_name,
            parent,
            repository_name,
            path=path,
            parent_path=get_path_parent(path),
        )

    @classmethod
    def create_from_external_dependency(
        cls,
        package: str,
        repository_name: str,
    ) -> "Package":
        """Creates a Package instance from an external dependency.

        Args:
            package (str): The dependency name.
            repository_name (str): The name of the associated repository.

        Returns:
            Package: A Package instance.
        """
        parent, name = get_package_parent_and_name(package)
        return Package(name, package, parent, repository_name, external=True)

    def __init__(
        self,
        name: str,
        canonical_name: str,
        parent_package: str,
        repository_name: str,
        path: Optional[str] = None,
        parent_path: Optional[str] = None,
        external: bool = False,
        identity: Optional[int] = None,
        inferred: bool = False,
    ):
        """Constructor

        Args:
            name (str): The name of the package.
            canonical_name (str): The full canonical name (including all parents) of the package.
            parent_package (str): The canonical name of the package.
            repository_name (str): The name of the repository.
            path (Optional[str], optional): The path of the package. Defaults to None.
            parent_path (Optional[str], optional): The path of the parent package. Defaults to None.
            external (bool, optional): Whether the package is an external dependency of
                                       the repository. Defaults to False.
            identity (int, optional): Optional Node identity
        """
        super().__init__(
            identity=identity,
            name=name,
            canonical_name=canonical_name,
            parent_package=parent_package,
            path=path,
            parent_path=parent_path,
            external=external,
            repository_name=repository_name,
            inferred=inferred,
        )


class Module(Node):
    """Represents a Module within the repository.

    Attributes:
        name (str): The file.
        path (str): The file path within the repository.
        extension (str): The file extension.
        is_test (bool): Whether the file has been assessed to be a test file.
        inferred (bool): This object was inferred when parsing dependencies or calls. Default False.
    """

    name: str
    canonical_name: Optional[str] = None
    path: Optional[str] = None
    parent_path: Optional[str] = None
    extension: str = PYTHON_EXTENSION
    is_test: bool = False
    inferred: bool = False

    def __hash__(self):
        return hash((self.name, self.path))

    def __eq__(self, other):
        return (self.name, self.path) == (other.name, other.path)

    def update_canonical_name(self, canonical_name: str) -> "Module":
        """Update the canonical name of a Module.

        Args:
            canonical_name (str): The canonical name to update.

        Returns:
            Module: New Module object.
        """
        return Module(
            canonical_name=canonical_name,
            name=self.name,
            path=self.path,
            parent_path=self.parent_path,
            extension=self.extension,
            is_test=self.is_test,
            repository_name=self.repository_name,
            inferred=self.inferred,
        )

    @classmethod
    def create_init_module(
        cls, parent_canonical_name: str, repository_name: str
    ) -> "Module":
        """Create an __init__ module for a Package.

        Args:
            parent_canonical_name (str): The canonical name of the parent Package.
            repository_name (str): The name of the associated repository.

        Returns:
            Module: __init__
        """
        return Module(
            name="__init__",
            canonical_name=f"{parent_canonical_name}.__init__",
            repository_name=repository_name,
            inferred=True,
        )


class Class(Node):
    """Represents a Python class.

    Attributes:
        name (str): The class name.
        min_line_number (Optional[int]): The first line of the class definition.
        max_line_number (Optional[int): The last line of the class definition.
        inferred (bool): This object was inferred when parsing dependencies or calls. Default False.
    """

    name: str
    canonical_name: Optional[str] = None
    min_line_number: Optional[int] = None
    max_line_number: Optional[int] = None
    inferred: bool = False


class Function(Node):
    """Represents a Python function or method.

    Attributes:
        name (str): The name of the function or method.
        type (FunctionType): Whether this is a function or a method.
        builtin (bool): Whether the function is a Python interpreter built-in function.
        source_code (Optional[str]): The original source code string.
        ast (Optional[ast.AST]): Abstract Syntax Tree extracted from the source code.
        min_line_number (Optional[int]): The first line of the function definition.
        max_line_number (Optional[int]): The last line of the function definition.
        inferred (bool): This object was inferred when parsing dependencies or calls. Default False.
    """

    class FunctionType(Enum):
        """Enum for FunctionType.

        Either Method or Function.
        """

        METHOD = "Method"
        FUNCTION = "Function"

    name: str
    type: FunctionType
    builtin: bool = False
    canonical_name: Optional[str] = None
    source_code: Optional[str] = None
    ast: Optional[Any] = Field(default=None, exclude=True)
    min_line_number: Optional[int] = None
    max_line_number: Optional[int] = None
    inferred: bool = False


class Variable(Node):
    """Represents a Python variable.

    Attributes:
        name (str): The variable name
        type (str): The inferred type of the variable, usually from a type hint.
        inferred (bool): This object was inferred when parsing dependencies or calls. Default False.
    """

    name: str
    canonical_name: str
    type: Optional[str] = "Any"
    inferred: bool = False


class Argument(Node):
    """Node representing an argument to a function.

    Attributes:
        name (str): The variable name
        type (str): The inferred type of the variable, usually from a type hint.
    """

    name: Optional[str] = None
    type: Optional[str] = "Any"


class ReturnValue(Node):
    """Node representing a return value from a function.

    Attributes:
        name (str): The variable name
        type (str): The inferred type of the variable, usually from a type hint.
    """

    name: Optional[str] = None
    type: Optional[str] = "Any"


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

    short_description: Optional[str] = None
    long_description: Optional[str] = None
    summarization: Optional[str] = None


class DocstringArgument(Argument):
    """Represents an argument description with a docstring.

    Attributes:
        name (str): The argument name.
        description (str): The description of the argument.
        type (str): The inferred type of the variable, usually from a type hint.
        is_optional (bool): Whether the argument is optional.
        default (Optional[Any]): The default value of the argument, if it is optional.
    """

    description: Optional[str] = None
    is_optional: bool
    default: Optional[Any] = None


class DocstringReturnValue(ReturnValue):
    """Represents a return value description within a docstring.

    Attributes:
        name (str): The argument name.
        description (str): The description of the argument.
        type (str): The inferred type of the variable, usually from a type hint.
        is_generator (bool): Whether the return value is a generator.
    """

    description: Optional[str] = None
    is_generator: bool


class DocstringRaises(Node):
    """Represents a raises/exception descritpion within a docstring.

    Args:
        description (str): The description of the exception that may be raised.
        type (str): The inferred type of the exception, usually from a type hint.
    """

    description: str
    type: Optional[str] = None
