"""
RepographBuilder generates a populated Repograph from inspect4py JSON output.
"""
# Base imports
import logging
import os
from typing import Callable, Dict, Set, List, Optional, Tuple, Union

from py2neo import Transaction

# Build entity imports
from repograph.entities.build.exceptions import RepographBuildError
from repograph.entities.graph.service import GraphService

# Models imports
from repograph.entities.graph.models.nodes import (
    Argument,
    Class,
    Docstring,
    DocstringArgument,
    DocstringRaises,
    DocstringReturnValue,
    Directory,
    Module,
    Function,
    License,
    Package,
    README,
    Repository,
    ReturnValue,
    Variable,
)
from repograph.entities.graph.models.relationships import (
    Calls,
    Contains,
    Describes,
    Documents,
    HasArgument,
    HasFunction,
    HasMethod,
    Imports,
    LicensedBy,
    Returns,
    Requires,
)

# Utility imports
from repograph.utils.builtin import PYTHON_BUILT_IN_FUNCTIONS
from repograph.utils.json import (
    JSONDict,
    convert_dependencies_map_to_set,
    parse_min_max_line_numbers,
    marshall_json_to_string,
)
from repograph.entities.build.utils import find_node_object_by_name
from repograph.utils.paths import (
    strip_file_path_prefix,
    is_root_folder,
    get_path_name,
    get_path_root,
    get_path_parent,
    get_package_parent_and_name,
    get_module_and_object_from_canonical_object_name,
)

ADDITIONAL_KEYS = ["requirements", "directory_tree", "license", "readme_files"]

INIT = "__init__"

log = logging.getLogger("repograph.repograph_builder")


class RepographBuilder:
    """
    Generates a Repograph from inspect4py output.
    """

    def __init__(
        self,
        summarize: Optional[Callable[[Function], str]],
        base_path: str,
        graph_name: str,
        graph: GraphService,
        tx: Transaction,
    ) -> None:
        """Constructor

        Args:
            summarize (Optional[Callable[[Function], str]]): The optional summarization method.
            base_path (str): The base path directory
            graph_name (str): The name of the graph nodes are being added to.
        """
        # The base directory path used for normalizing paths
        self.base_path = base_path

        # Name of the graph. Used for calls to the graph service
        self.graph_name = graph_name

        # The name of the repository
        self.repository_name = ""

        # Transaction to use for calls to the graph service
        self.tx = tx

        # Graph service
        self.graph: GraphService = graph

        # The optional summarization function
        self.summarize: Optional[Callable[[Function], str]] = summarize

        # Mapping of paths to Directory (or the Repository) object
        self.directories: Dict[str, Union[Repository, Directory]] = dict()

        # Mapping of paths/pacakge names to modules
        self.modules: Dict[str, Module] = dict()

        # Mapping of Module objects to Classes/Function objects
        self.module_objects: Dict[Module, List[Union[Class, Function]]] = dict()

        # Mapping Module dependencies for retrospective parsing
        self.dependencies: List[Tuple[List[JSONDict], Module]] = []

        # The objects a given Module depends on/imports
        self.module_dependencies: Dict[Module, List[Union[Module, Function]]] = dict()

        # Module imports
        self.module_imports: Dict[Module, Set[str]] = dict()

        # Packages from requirements file
        self.requirements: Dict[str, Package] = dict()

        # Mapping of built-in functions that have been called in the repository
        self.called_builtin_functions: Dict[str, Function] = dict()

    def _parse_repository(
        self,
        path: str,
        metadata: JSONDict = None,
        software_type: str = None,
        directory_info: List[JSONDict] = None,
    ) -> Repository:
        """Parses information about the repository, i.e. the root,
        itself.

        Args:
            path (str): The path of the repository.
            metadata (Optional[JSONDict]): Optional metadata describing the repository.
            directory_info (Optional[List[JSONDict]]): Optional list of directories to parse

        Returns:
            Repository: The created Repository node
        """
        is_package = False
        modules = []

        # Parse files within this folder, as Python files may be contained in the repository root
        if directory_info:
            modules, is_package = self._parse_files_in_directory(directory_info)

        if metadata:
            repository = Repository.create_from_metadata(
                path, metadata, is_package, software_type, path
            )
        else:
            repository = Repository(
                name=path,
                is_root_package=is_package,
                type=software_type,
                repository_name=path,
            )

        self.repository_name = repository.name

        self.graph.add(repository, tx=self.tx, graph_name=self.graph_name)
        self.directories[repository.name] = repository

        # Parse each extracted module
        for module, file_info in modules:
            # If repository root is a package, add the full canonical name as such
            if repository.is_root_package:
                module = module.update_canonical_name(
                    f"{repository.name}.{module.name}"
                )

            # Now parse the contents of the  module
            self._parse_module_contents(module, file_info)

            # Create a relationship between the Repository and the Module
            relationship = Contains(repository, module, self.repository_name)
            self.graph.add(module, tx=self.tx, graph_name=self.graph_name)
            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

            # Finally add the module to the list of stored modules
            self.modules[module.canonical_name] = module
            self.modules[module.path] = module

        return repository

    def _parse_requirements(
        self, requirements: Optional[JSONDict], repository: Repository
    ) -> None:
        """Parses information extracted from the requirements.txt file.

        Args:
            requirements (Optional[JSONDict]): The JSON describing the requirements.
                                               May be None if not found.
            repository (Repository): The parent Repository node for any created
                                     Package nodes.
        """
        if not requirements:
            log.warning("No requirements information found.")
        else:
            log.info("Parsing requirements information...")
            for requirement, version in requirements.items():
                package = Package.create_from_external_dependency(
                    requirement, self.repository_name
                )
                relationship = Requires(
                    repository,
                    package,
                    self.repository_name,
                    version=version,
                )
                self.graph.add(package, tx=self.tx, graph_name=self.graph_name)
                self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)
                self.requirements[requirement] = package

    def _parse_license(
        self, licenses: Optional[JSONDict], repository: Repository
    ) -> None:
        """Parses extracted license information.

        Args:
            licenses (Optional[JSONDict]): The JSON describing the extracted licenses.
            repository (Repository): The parent Repository node for any created License nodes.

        Returns:
            None
        """
        if not licenses:
            log.warning("No license information found.")
        else:
            log.info("Parsing repository license information.")
            detected_types = licenses.get("detected_type", [])
            if len(detected_types) == 0:
                log.warning("No license types detected")

            for detected in detected_types:
                for detected_type, confidence in detected.items():
                    license_node = License(
                        text=licenses.get("extracted_text", None),
                        license_type=detected_type,
                        confidence=(float(confidence.strip("%")) / 100),
                        graph_name=self.graph_name,
                        repository_name=self.repository_name,
                    )
                    relationship = LicensedBy(
                        repository, license_node, self.repository_name
                    )
                    self.graph.add(license_node, tx=self.tx, graph_name=self.graph_name)
                    self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

    def _parse_readme(self, info: JSONDict):
        """Parse README files in the repository

        Args:
            info (JSONDict): README files information.

        Returns:
            None
        """
        log.info("Parsing README files...")
        if not info:
            log.warning("No READMEs found!")
            return

        readmes = []
        relationships = []
        from pathlib import Path

        for path, content in info.items():
            path = str(Path(path).relative_to(self.base_path))
            readme = README(
                path=path,
                content=content,
                graph_name=self.graph_name,
                repository_name=self.repository_name,
            )
            readmes.append(readme)

            parent_path = get_path_parent(path)
            parent = self.directories.get(parent_path, None)

            if parent:
                relationship = Contains(parent, readme, self.repository_name)
                relationships.append(relationship)
            else:
                log.error("Couldn't find parent for README at path: %s", path)

        self.graph.add(*readmes, tx=self.tx, graph_name=self.graph_name)
        self.graph.add(*relationships, tx=self.tx, graph_name=self.graph_name)

    def _get_parent_directory(self, parent_path: str) -> Directory:
        """Retrieves the parent directory for supplied path.

        Recursively creates missing parent directories and adds relationship.

        Args:
            parent_path (str): The path the parent directory to retrieve

        Returns:
            Type[Directory]: The parent Directory.
        """

        def add_parents_recursively(child: Directory) -> None:
            """Recursively adds further missing parent directories

            Args:
                child (Directory): The immediate parent directory to the true child directory.
                                   i.e. the Directory with the path of parent_path.

            Returns:
                None
            """
            parent = self.directories.get(child.parent_path, None)

            if not parent:
                parent = Directory(child.parent_path, self.repository_name)
                relationship = Contains(parent, child, self.repository_name)
                self.graph.add(parent, tx=self.tx, graph_name=self.graph_name)
                self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)
                self.directories[parent.path] = parent
                return add_parents_recursively(parent)
            else:
                parent_relationship = Contains(parent, child, self.repository_name)
                self.graph.add(child, tx=self.tx, graph_name=self.graph_name)
                self.graph.add(
                    parent_relationship, tx=self.tx, graph_name=self.graph_name
                )
                return

        # Attempt to get the parent directory from the list of created directories.
        existing_parent = self.directories.get(parent_path, None)
        if existing_parent:
            return existing_parent

        # If it doesn't exist create a new Directory and then call the recursive function.
        new_parent = Directory(parent_path, self.repository_name)
        self.graph.add(new_parent, tx=self.tx, graph_name=self.graph_name)
        self.directories[new_parent.path] = new_parent
        add_parents_recursively(new_parent)

        return new_parent

    def _create_canonical_package_name(self, directory_path: str) -> str:
        """Create canonical package name for a directory path

        Args:
            directory_path (str): The starting directory.

        Returns:
            str: The canonical package name.
        """
        parts = [get_path_name(directory_path)]
        parent = get_path_parent(directory_path)

        while parent != "":
            parent_node = self.directories.get(parent, None)

            if isinstance(parent_node, Package) or (
                isinstance(parent_node, Repository) and parent_node.is_root_package
            ):
                parts = [get_path_name(parent)] + parts
                parent = get_path_parent(parent)
            else:
                return ".".join(parts)

        return ".".join(parts)

    def _parse_directory(
        self,
        directory_name: str,
        directory_info: List[JSONDict],
        index: int,
        total: int,
    ) -> None:
        """Parse a directory

        Args:
            directory_name (str): The name of the directory.
            directory_info (JSONDict): The directory information.
            index (int): The index of the directory within the repository.
            total (int): The total number of directories within the repository.
        """
        directory_path = strip_file_path_prefix(directory_name)
        log.debug("Parsing directory '%s' (%d/%d)", directory_path, index + 1, total)

        # Parse each file within the directory, update is_package
        # with result (whether file is __init__.py), and add to list
        # of Files.
        modules, is_package = self._parse_files_in_directory(directory_info)

        # Get the parent directory
        parent = self._get_parent_directory(get_path_parent(directory_path))

        # If an __init__.py was found, create a Package node,
        # otherwise create a Directory node.
        if is_package:
            canonical_name = self._create_canonical_package_name(directory_path)
            directory = Package.create_from_directory(
                directory_path, canonical_name, self.repository_name
            )
        else:
            directory = Directory(directory_path, self.repository_name)

        # Add the list of created directories, the directory node,
        # and the relationship to its parent, to the Repograph.
        self.directories[directory.path] = directory
        relationship = Contains(parent, directory, self.repository_name)
        self.graph.add(parent, tx=self.tx, graph_name=self.graph_name)
        self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

        # Parse each extracted module
        for module, file_info in modules:
            # If parent is a package, add the full canonical path name and add to modules.
            if isinstance(directory, Package):
                module = module.update_canonical_name(
                    f"{directory.canonical_name}.{module.name}"
                )
                self.modules[module.canonical_name] = module

            # Now parse the contents of the module.
            self._parse_module_contents(module, file_info)

            # Create a relationship between the Directory and the Module.
            relationship = Contains(directory, module, self.repository_name)
            self.graph.add(module, tx=self.tx, graph_name=self.graph_name)
            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

            # Finally add the module to the list of stored modules.
            self.modules[module.path] = module
            self.modules[module.canonical_name] = module

    def _parse_files_in_directory(
        self, directory_info: List[JSONDict]
    ) -> Tuple[List[Tuple[Module, JSONDict]], bool]:
        """Parses files within a directory into Python Module nodes.

        Args:
            directory_info (List[JSONDict]): The list of JSONDict objects to parse.

        Returns:
            Tuple[List[Tuple[Module, JSONDict]], bool]: The list of parsed Module nodes and whether
                                                        the enclosing directory is a package.
        """
        is_package = False
        modules = []

        for file_index, file_info in enumerate(directory_info):
            module = self._parse_module(file_info, file_index, len(directory_info))
            is_package = is_package or module.name == INIT
            modules.append((module, file_info))

        return modules, is_package

    def _parse_module(self, file_info: JSONDict, index: int, total: int) -> Module:
        """Parses a Python module with a parent directory.

        Args:
            file_info (JSONDict): The information about the file to parse.
            index (int): The index of the Module within the parent Folder.
            total (int): The total number of Modules within the parent Folder.

        Returns:
            bool: Whether Module is an __init__.py.
        """
        log.debug(
            "--> Parsing file `%s` (%d/%d)",
            file_info["file"]["fileNameBase"],
            index + 1,
            total,
        )

        module = Module(
            name=file_info["file"]["fileNameBase"],
            canonical_name=file_info["file"]["fileNameBase"],
            path=file_info["file"]["path"],
            parent_path=get_path_parent(file_info["file"]["path"]),
            extension=file_info["file"]["extension"],
            is_test=file_info.get("is_test", False),
            repository_name=self.repository_name,
        )

        self.module_objects[module] = []

        return module

    def _parse_module_contents(self, module: Module, file_info: JSONDict) -> None:
        """Parse the contents of the module.

        This includes functions/methods and classes.

        Args:
            module (Module): Module object to link extracted functions/classes to.
            file_info (JSONDict): The JSONDict of information containing information about
                                  the module.

        Returns:
            None
        """
        self._parse_functions_and_methods(file_info.get("functions", {}), module)
        self._parse_classes(file_info.get("classes", {}), module)

        if "dependencies" in file_info:
            self.dependencies.append((file_info["dependencies"], module))
            self.module_imports[module] = convert_dependencies_map_to_set(
                file_info["dependencies"]
            )

    def _parse_functions_and_methods(
        self,
        functions_info: JSONDict,
        parent: Union[Module, Class],
        methods: bool = False,
    ) -> None:
        """Parses function/method information into Function/Method nodes and adds links
        to the parent File/Class node.

        Args:
            functions_info (JSONDict): JSON dictionary containing the function information.
            parent (Union[Module, Class]): Parent File or Class node.
            methods (bool): Whether to create Method nodes rather than Function nodes.
        """
        for name, info in functions_info.items():
            # Get min-max line numbers
            min_lineno, max_lineno = parse_min_max_line_numbers(info)
            if not min_lineno or not max_lineno:
                log.warning("Missing line number information for function '%s'", name)

            # Serialise the AST
            ast = info.get("ast")
            if ast:
                ast_string = marshall_json_to_string(ast)
                if not ast:
                    log.error("Couldn't serialise AST for function %s", name)
            else:
                log.warning("AST missing for function %s", name)
                ast_string = None

            # Check source_code is available
            source_code = info.get("source_code", None)
            if not source_code:
                log.warning("Source code missing for function %s", name)

            # Create Function Node
            if methods:
                function_type = str(Function.FunctionType.METHOD.value)
            else:
                function_type = str(Function.FunctionType.FUNCTION.value)

            function = Function(
                name=name,
                type=function_type,
                canonical_name=f"{parent.canonical_name}.{name}",
                source_code=source_code,
                ast=ast_string,
                min_line_number=min_lineno,
                max_line_number=max_lineno,
                repository_name=self.repository_name,
            )

            # Add to graph
            self.graph.add(function, tx=self.tx, graph_name=self.graph_name)

            # Parse the docstring for the function
            self._parse_docstring(info.get("doc", {}), function)

            # Create HasFunction Relationship
            if methods:
                relationship = HasMethod(parent, function, self.repository_name)
            else:
                relationship = HasFunction(parent, function, self.repository_name)
            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

            # If parent is a module, add to the module_objects set
            if isinstance(parent, Module):
                self.module_objects[parent].append(function)

            # Parse arguments and create Argument nodes
            self._parse_arguments(
                info.get("args", []), info.get("annotated_arg_types", {}), function
            )

            # Parse return values and create ReturnValue nodes
            self._parse_return_values(
                info.get("returns", []),
                info.get("annotated_return_type", "Any"),
                function,
            )

    def _parse_classes(self, class_info: Dict, parent: Module) -> None:
        """Parses class information into Class nodes and
        adds links to parent File node.

        Args:
            class_info (Dict): Dictionary containing class information.
            parent (Module): Parent File node.
        """
        for name, info in class_info.items():
            min_lineno, max_lineno = parse_min_max_line_numbers(info)
            class_node = Class(
                name=name,
                canonical_name=f"{parent.canonical_name}.{name}",
                min_line_number=min_lineno,
                max_line_number=max_lineno,
                repository_name=self.repository_name,
            )
            relationship = Contains(parent, class_node, self.repository_name)
            self.graph.add(class_node, tx=self.tx, graph_name=self.graph_name)
            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

            # Add to module objects set
            self.module_objects[parent].append(class_node)

            # Parse extends
            # self._parse_extends(info.get("extend", []), class_node)

            # Parse docstring
            self._parse_docstring(info.get("doc", {}), class_node)

            # Parse method info inside class if available
            methods_info = info.get("methods", None)
            if methods_info:
                self._parse_functions_and_methods(
                    methods_info, class_node, methods=True
                )

    def _parse_arguments(
        self,
        args_list: List[str],
        annotated_arg_types: Dict[str, str],
        parent: Function,
    ) -> None:
        """Parse arguments from method information.

        Args:
            args_list (List[str]): The list of argument names.
            annotated_arg_types (Dict[str, str]): The annotated argument types.
            parent (Function): The parent function the arguments belong to.
        """
        arg_types = annotated_arg_types
        for arg in args_list:
            if arg_types:
                arg_type = arg_types.get(arg, "Any")
            else:
                arg_type = "Any"

            argument = Argument(
                name=arg, type=arg_type, repository_name=self.repository_name
            )
            relationship = HasArgument(parent, argument, self.repository_name)
            self.graph.add(argument, tx=self.tx, graph_name=self.graph_name)
            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

    def _parse_return_values(
        self, return_values: List[List[str]], annotated_type: str, parent: Function
    ) -> None:
        """Parse return values from function/method information.

        Args:
            return_values (List[str]): The list of return value names.
            annotated_type (Dict[str, str]): The annotated return value types.
            parent (Function): The parent function the return values belong to.
        """
        if len(return_values) > 1:
            return_type = "Any"
        elif len(return_values) == 1:
            return_type = annotated_type
        else:
            return

        def parse(values):
            for value in values:
                if isinstance(value, list):
                    parse(value)
                elif isinstance(value, str):
                    return_value = ReturnValue(
                        name=value,
                        type=return_type,
                        repository_name=self.repository_name,
                    )
                    relationship = Returns(parent, return_value, self.repository_name)
                    self.graph.add(return_value, tx=self.tx, graph_name=self.graph_name)
                    self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)
                else:
                    log.error(
                        "Unexpected return value type `%s` for function `%s`",
                        type(value),
                        parent.name,
                    )

        parse(return_values)

    def _parse_docstring(
        self, docstring_info: Optional[JSONDict], parent: Union[Function, Class]
    ) -> None:
        """Parse docstring information for function or class

        Args:
            docstring_info (JSONDict): The JSONDict containing docstring information.
            parent (Union[Function, Class): The parent node the docstring describes.

        Returns:
            None
        """
        # Return immediately depending on whether Class/Function, if docstring info
        # provided, and whether summarization enabled.
        if isinstance(parent, Class):
            if not docstring_info or not bool(docstring_info):
                log.debug(f"No docstring information for class {parent.name}")
                return
        elif isinstance(parent, Function):
            if (not docstring_info or not bool(docstring_info)) and not self.summarize:
                log.debug(f"No docstring information for {parent.name}")
                return
        else:
            return

        # Initialise empty arrays for storing created nodes/relationships
        nodes = []
        relationships = []

        # If the summarization flag is set and parent is a Function (not a Class),
        # call the function summarizer.
        if self.summarize and isinstance(parent, Function):
            summary = self.summarize(parent)
        else:
            summary = None

        # Parse docstring
        docstring = Docstring(
            summarization=summary,
            short_description=docstring_info.get("short_description", None),
            long_description=docstring_info.get("long_description", None),
            repository_name=self.repository_name,
        )
        relationship = Documents(docstring, parent, self.repository_name)
        nodes.append(docstring)
        relationships.append(relationship)

        if isinstance(parent, Class):
            # Parse docstring arguments
            for arg, arg_info in docstring_info.get("args", {}).items():
                docstring_arg = DocstringArgument(
                    name=arg,
                    type=arg_info.get("type_name", None),
                    description=arg_info.get("description", None),
                    is_optional=arg_info.get("is_optional", False),
                    default=arg_info.get("default", None),
                    repository_name=self.repository_name,
                )
                relationship = Describes(docstring, docstring_arg, self.repository_name)
                nodes.append(docstring_arg)
                relationships.append(relationship)

            if "returns" in docstring_info:
                # Parse docstring return values
                returns_info = docstring_info.get("returns", {})
                docstring_return_value = DocstringReturnValue(
                    name=returns_info.get("return_name", None),
                    description=returns_info.get("description", None),
                    type=returns_info.get("type_name", None),
                    is_generator=returns_info.get("is_generator", False),
                    repository_name=self.repository_name,
                )
                relationship = Describes(
                    docstring, docstring_return_value, self.repository_name
                )
                nodes.append(docstring_return_value)
                relationships.append(relationship)

            # Parse docstring raises
            for raises in docstring_info.get("raises", []):
                docstring_raises = DocstringRaises(
                    description=raises.get("description", None),
                    type=raises.get("type_name", None),
                    repository_name=self.repository_name,
                )
                relationship = Describes(
                    docstring, docstring_raises, self.repository_name
                )
                nodes.append(docstring_raises)
                relationships.append(relationship)

        # Add nodes and relationships to graph
        self.graph.add(*nodes, tx=self.tx, graph_name=self.graph_name)
        self.graph.add(*relationships, tx=self.tx, graph_name=self.graph_name)

    def _parse_dependencies(self) -> None:  # noqa: C901
        """Parse the dependencies between Modules.

        Returns:
            None
        """
        log.info("Parsing dependencies...")
        unresolved_dependencies = []

        # Iterate through dependencies for each required module
        for dependency_info, module in self.dependencies:
            # Create an entry in the module_dependencies dict,
            # so we can keep track of found objects.
            self.module_dependencies[module] = []

            # Iterate through each dependency in the module
            for dependency in dependency_info:
                # Check whether a module object or module itself is being imported
                if "from_module" in dependency:
                    imports_module = False
                else:
                    imports_module = True

                # Get the imported object (either module or object)
                imported_object = dependency["import"]
                source_module = dependency.get("from_module", imported_object)

                # Find the module
                if dependency["type"] == "internal":
                    imported_module = self.modules.get(source_module, None)
                    # If we can't find the module, it could be a relative import so use the package
                    # components if the importing module's canonical name.
                    if not imported_module:
                        added = []
                        for part in module.canonical_name.split("."):
                            added.append(part)
                            imported_module = self.modules.get(
                                ".".join(added + [source_module]), None
                            )
                            if imported_module:
                                break
                    # Finally if we still haven't found the imported module, it may be the case that
                    # the object is being imported from the __init__ of a package.
                    if not imported_module:
                        imported_module = self.modules.get(
                            f"{source_module}.__init__", None
                        )

                else:
                    imported_module = self.modules.get(source_module, None)
                    if not imported_module:
                        imported_module = self.modules.get(
                            f"{source_module}.__init__", None
                        )

                # If importing a module directly....
                if imports_module:
                    # ...and it already exists create the relationship
                    if imported_module:
                        self.graph.add(
                            Imports(module, imported_module, self.graph_name),
                            tx=self.tx,
                            graph_name=self.graph_name,
                        )
                        self.module_dependencies[module].append(imported_module)
                    # ...and if it doesn't recursively create it
                    else:
                        source_module, missing = self._calculate_missing_packages(
                            source_module
                        )

                        if source_module == "":
                            child = self._create_missing_nodes(missing)
                        elif source_module in self.requirements:
                            child = self._create_missing_nodes(
                                missing, parent=self.requirements[source_module]
                            )
                        else:
                            child = self._create_missing_nodes(
                                missing, parent=self.modules[source_module]
                            )

                        self.module_dependencies[module].append(child)

                # If importing a class, function, etc...
                else:
                    # ...or it already exists then create the relationship
                    if imported_module:
                        if imported_module.inferred:
                            if imported_object[0].isupper():
                                imported_object = Class(
                                    name=imported_object,
                                    canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                                    repository_name=self.repository_name,
                                    inferred=True,
                                )
                            else:
                                imported_object = Function(
                                    name=imported_object,
                                    canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                                    type=str(Function.FunctionType.FUNCTION.value),
                                    repository_name=self.repository_name,
                                    inferred=True,
                                )

                            self.graph.add(
                                Imports(module, imported_object, self.graph_name),
                                Imports(
                                    imported_module, imported_object, self.graph_name
                                ),
                                tx=self.tx,
                                graph_name=self.graph_name,
                            )

                            self.module_dependencies[imported_module].append(
                                imported_object
                            )
                            self.module_dependencies[module].append(imported_object)
                        else:
                            module_objects = self.module_objects.get(
                                imported_module, []
                            )
                            if not module_objects:
                                unresolved_dependencies.append(
                                    (
                                        module,
                                        imported_module,
                                        imported_object,
                                        dependency,
                                    )
                                )
                                continue

                            # Filter the module objects for only those with the imported name
                            matching_objects = [
                                obj
                                for obj in module_objects
                                if obj is not None and obj.name == imported_object
                            ]

                            # If no matches, log an error and move onto the next dependency
                            if len(matching_objects) == 0:
                                unresolved_dependencies.append(
                                    (
                                        module,
                                        imported_module,
                                        imported_object,
                                        dependency,
                                    )
                                )
                                continue

                            # If more than one match we log this inconsistency,
                            # but add all import relationships
                            if len(matching_objects) > 1:
                                log.warning(
                                    "More than 1 matching object found in import."
                                )

                            for match in matching_objects:
                                self.graph.add(
                                    Imports(module, match, self.repository_name),
                                    tx=self.tx,
                                )
                                self.module_dependencies[module].append(match)
                    # ...and if it doesn't recursively create it
                    else:
                        if imported_object[0].isupper():
                            imported_object = Class(
                                name=imported_object,
                                canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                                repository_name=self.repository_name,
                                inferred=True,
                            )
                        else:
                            imported_object = Function(
                                name=imported_object,
                                canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                                type=str(Function.FunctionType.FUNCTION.value),
                                repository_name=self.repository_name,
                                inferred=True,
                            )

                        source_module, missing = self._calculate_missing_packages(
                            source_module
                        )

                        if source_module == "":
                            self._create_missing_nodes(missing)
                        elif source_module in self.requirements:
                            self._create_missing_nodes(
                                missing,
                                parent=self.requirements[source_module],
                                import_object=imported_object,
                            )
                        else:
                            self._create_missing_nodes(
                                missing,
                                parent=self.modules[source_module],
                                import_object=imported_object,
                            )

                        self.graph.add(
                            Imports(module, imported_object, self.repository_name),
                            tx=self.tx,
                            graph_name=self.graph_name,
                        )
                        self.module_dependencies[module].append(imported_object)

        # Second pass on unresolved dependencies that are likely to be imports of other modules.
        unresolved = unresolved_dependencies
        while len(unresolved) != 0:
            remaining = []
            for (
                module,
                imported_module,
                imported_object,
                dependency,
            ) in unresolved:
                # Check the module objects of the imported module first
                module_objects = self.module_objects.get(imported_module, [])
                matching_objects = [
                    obj
                    for obj in module_objects
                    if obj is not None and obj.name == imported_object
                ]
                if len(matching_objects) > 0:
                    for match in matching_objects:
                        self.graph.add(
                            Imports(module, match, self.repository_name), tx=self.tx
                        )
                        self.module_dependencies[module].append(match)
                    continue

                # Then check the module imports of the imported module
                module_imports = self.module_dependencies.get(imported_module, [])
                matching_objects = [
                    obj
                    for obj in module_imports
                    if obj is not None and obj.name == imported_object
                ]
                if len(matching_objects) > 0:
                    for match in matching_objects:
                        self.graph.add(
                            Imports(module, match, self.repository_name), tx=self.tx
                        )
                        self.module_dependencies[module].append(match)
                    continue

                remaining.append((module, imported_module, imported_object, dependency))

            if len(remaining) == len(unresolved):
                unresolved = remaining
                break
            else:
                unresolved = remaining

        # Finally, infer any remaining objects
        for (
            module,
            imported_module,
            imported_object,
            dependency,
        ) in unresolved:
            if imported_object.isupper() or imported_object.startswith("__"):
                imported_object = Variable(
                    name=imported_object,
                    canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                    inferred=True,
                    repository_name=self.repository_name,
                )
            elif imported_object[0].isupper():
                imported_object = Class(
                    name=imported_object,
                    canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                    repository_name=self.repository_name,
                    inferred=True,
                )
            else:
                imported_object = Function(
                    name=imported_object,
                    canonical_name=f"{dependency['from_module']}.{dependency['import']}",
                    type=str(Function.FunctionType.FUNCTION.value),
                    repository_name=self.repository_name,
                    inferred=True,
                )

            self.graph.add(
                Contains(imported_module, imported_object, self.repository_name),
                Imports(module, imported_object, self.repository_name),
                tx=self.tx,
                graph_name=self.graph_name,
            )
            self.module_objects[imported_module].append(imported_object)
            self.module_dependencies[module].append(imported_object)

    def _calculate_missing_packages(self, source_module: str) -> Tuple[str, List[str]]:
        """Calculates missing packages for a given import source Module.

        Checks both parsed Modules and Repository level requirements.

        Args:
            source_module (str): The canonical name of the source module.

        Returns:
            str: Any pre-existing source package.
            List[str]: Missing packages/modules.
        """
        missing = []
        while (
            source_module not in self.modules
            and source_module not in self.requirements
            and source_module != ""
        ):
            parent, child = get_package_parent_and_name(source_module)
            missing.append(child)
            source_module = parent

        return source_module, missing

    def _create_missing_nodes(
        self,
        missing: List[str],
        parent: Package = None,
        import_object: Union[Class, Function] = None,
    ) -> Union[Module, Function]:
        """Create missing nodes.

        Args:
            missing (List[str]):
            parent (Package): The parent Package. Optional.
            import_object (Union[Class, Function]): The Class or Function being imported from the

        Returns:
            Union[Module, Function]: The child Node.
        """
        nodes = []
        relationships = []
        child = None

        for index, m in enumerate(missing):
            if index == len(missing) - 1:
                new = Module(
                    name=m, repository_name=self.repository_name, inferred=True
                )
                child = new
            else:
                new = Package(
                    name=m,
                    canonical_name=f"{parent.canonical_name}.{m}" if parent else m,
                    parent_package=parent.canonical_name if parent else "",
                    external=True,
                    repository_name=self.repository_name,
                    inferred=True,
                )

            if parent:
                relationships.append(Contains(parent, new, self.repository_name))

            parent = new
            nodes.append(new)

        # If we have an import_object, but the parent is a Package, we check to see if an __init__
        # module exists for the package. If not, we create an __init__ Module as this is actually
        # where the import_object is being imported from.
        if import_object and parent and isinstance(parent, Package):
            init_name = f"{parent.canonical_name}.__init__"
            if init_name in self.modules:
                parent = self.modules[init_name]
            else:
                new = Module.create_init_module(
                    parent.canonical_name, self.repository_name
                )
                relationships.append(Contains(parent, new, self.repository_name))
                self.modules[init_name] = new
                self.module_dependencies[new] = []
                parent = new

        # If we have an import object, create a Contains relationship with the parent module.
        if import_object:
            relationships.append(Contains(parent, import_object, self.repository_name))
            child = import_object

        # Add the created nodes and relationships to the Repograph.
        self.graph.add(*nodes, tx=self.tx, graph_name=self.graph_name)
        self.graph.add(*relationships, tx=self.tx, graph_name=self.graph_name)

        return child

    def _parse_extends(self, extends_info: List[str], class_node: Class) -> None:
        """Parse extends/super class information for a Class node.

        Args:
            extends_info (List[str]): The names of Classes that the Class node extends.
            class_node (Class): The Class node itself.

        Returns:
            None
        """
        if len(extends_info) == 0:
            log.debug(
                "Class `%s` doesn't not extend any other classes", class_node.name
            )
            return

        # for extends in extends_info:
        #     super_class = Class(name=extends, graph_name=self.graph_name)
        #     relationship = Extends(class_node, super_class, self.graph_name)
        #     self.repograph.add(super_class, relationship)

    def _parse_call_graph(self, call_graph: Optional[JSONDict]) -> None:
        """Parse the call graph extracted by inspect4py.

        Args:
            call_graph (Optional[JSONDict]): The call graph.

        Returns:
            None
        """
        if not call_graph:
            log.error("No call graph provided!")
            return

        for directory, files in call_graph.items():
            for file_name, file_info in files.items():
                module = self.modules.get(file_name)
                if not module:
                    log.error("Couldn't find existing Module node. Skipping!")
                    continue

                module_objects = self.module_objects.get(module, [])
                module_imports = self.module_imports.get(module, set())
                module_dependencies = self.module_dependencies.get(module, [])

                # Parse body calls
                self._parse_calls(
                    module,
                    file_info.get("body", {}),
                    module_objects,
                    module_imports,
                    module_dependencies,
                )

                # For each function described in the call graph, parse these calls
                for function_name, function_calls in file_info.get(
                    "functions", {}
                ).items():
                    function = find_node_object_by_name(module_objects, function_name)
                    self._parse_calls(
                        module,
                        function_calls,
                        module_objects,
                        module_imports,
                        module_dependencies,
                        caller=function,
                    )

        # Add called builtin functions to the graph
        self.graph.add(
            *self.called_builtin_functions.values(),
            tx=self.tx,
            graph_name=self.graph_name,
        )

    def _parse_calls(
        self,
        parent_module: Module,
        call_info: Optional[JSONDict],
        module_objects: List[any],
        module_imports: Set[str],
        module_dependencies: List[any],
        caller: Optional[Function] = None,
    ) -> None:
        """Parse the call graph for a particular module.

        Args:
            parent_module (Module): The parent module.
            call_info (Optional[JSONDict]): The call info.
            caller (Optional[Function): An optional specific function that the call info is for.
        Returns:
            None
        """
        if not call_info:
            return

        for call in call_info.get("local", []):
            module, function = get_module_and_object_from_canonical_object_name(call)
            matching_objects_in_module = find_node_object_by_name(
                module_objects, function
            )

            # If the call is to an imported function...
            if call in module_imports:
                matching_imports = find_node_object_by_name(module_dependencies, call)
                relationship = Calls(
                    caller if caller else parent_module,
                    matching_imports,
                    self.repository_name,
                )
            # ...or if the call is to a built-in function...
            elif call in PYTHON_BUILT_IN_FUNCTIONS:
                if function in self.called_builtin_functions:
                    function_node = self.called_builtin_functions[function]
                else:
                    function_node = Function(
                        name=function,
                        type=str(Function.FunctionType.FUNCTION.value),
                        builtin=True,
                        repository_name=self.repository_name,
                        inferred=True,
                    )
                    self.called_builtin_functions[function] = function_node

                # Create the relationship between the caller and the new function_node
                relationship = Calls(
                    caller if caller else parent_module,
                    function_node,
                    self.repository_name,
                )

            # ...or if the call is to a function defined in the module
            elif matching_objects_in_module:
                relationship = Calls(
                    caller if caller else parent_module,
                    matching_objects_in_module,
                    self.repository_name,
                )
            else:
                log.debug("Call to some other variable (%s). Ignoring.", call)
                relationship = None

            self.graph.add(relationship, tx=self.tx, graph_name=self.graph_name)

    def build(
        self,
        directory_info: Optional[JSONDict],
        call_graph: Optional[JSONDict],
    ) -> None:
        """Build a repograph from directory_info JSON.

        Args:
            directory_info (JSONDict): Directory info JSON.
            call_graph (Optional[JSONDict]): The call graph JSON.

        Returns:
            Repograph

        Raises:
            RepographBuildError
        """
        log.info("Building Repograph...")

        if not directory_info:
            log.error("Directory info is empty! Aborting!")
            raise RepographBuildError("Directory info is empty")

        # Pop off non-directory entries from the JSON, for parsing later
        requirements = directory_info.pop("requirements", None)
        _ = directory_info.pop("directory_tree", None)
        licenses = directory_info.pop("license", None)
        readmes = directory_info.pop("readme_files", None)
        metadata = directory_info.pop("metadata", None)
        _ = directory_info.pop("software_invocation", None)
        software_type = directory_info.pop("software_type", None)
        _ = directory_info.pop("tests", None)

        # Create a sorted list of directory paths.py, as dictionaries are not
        # always sortable in Python.
        log.info("Sorting directories with hierarchical ordering...")
        directories = sorted(
            list(directory_info.keys()),
            key=lambda file: (os.path.dirname(file), os.path.basename(file)),
        )

        # Parse repository root folder if it exists, otherwise manually create
        # the repository node.
        path = strip_file_path_prefix(directories[0])
        self.repository_name = path

        if is_root_folder(path):
            directory = directories.pop(0)
            repository = self._parse_repository(
                path,
                directory_info=directory_info[directory],
                metadata=metadata,
                software_type=software_type,
            )
        else:
            repository = self._parse_repository(
                get_path_root(path), metadata=metadata, software_type=software_type
            )

        # Parse requirements
        self._parse_requirements(requirements, repository)

        # Parse license
        self._parse_license(licenses, repository)

        # Parse each directory
        log.info("Extracting information from directories...")
        for index, directory in enumerate(directories):
            self._parse_directory(
                directory, directory_info[directory], index, len(directories)
            )

        # Retrospectively parse module dependencies
        log.info("Parsing module dependencies...")
        self._parse_dependencies()

        # Parse the call list, now that most Nodes should be added to the graph
        log.info("Parsing call graph...")
        self._parse_call_graph(call_graph)

        # Parse READMEs
        self._parse_readme(readmes)

        log.info("Successfully built a Repograph!")
