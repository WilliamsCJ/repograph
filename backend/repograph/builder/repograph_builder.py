"""
RepographBuilder generates a populated Repograph from inspect4py JSON output.
"""
import logging
import os
from typing import Dict, Set, List, Optional, Tuple, Union

from repograph.builder.function_summarizer import FunctionSummarizer
from repograph.repograph import Repograph
from repograph.models.nodes import Argument, Class, Docstring, DocstringArgument, \
                                   DocstringRaises, DocstringReturnValue, Directory, Module, \
                                   Function, License, Package, Repository, ReturnValue
from repograph.models.relationships import Contains, Describes, Documents, Extends, HasArgument, \
                                           HasFunction, HasMethod, LicensedBy, Returns, \
                                           Requires
from repograph.utils.json import JSONDict, parse_min_max_line_numbers, \
    marshall_json_to_string
from repograph.utils.paths import strip_file_path_prefix, is_root_folder, get_path_name, \
                                  get_path_root, get_path_parent

ADDITIONAL_KEYS = [
  "requirements",
  "directory_tree",
  "license",
  "readme_files"
]

INIT = "__init__"

log = logging.getLogger('repograph.repograph_builder')


class RepographBuilder:
    repograph: Repograph
    function_summarizer: FunctionSummarizer
    summarize: bool
    directories: Dict[str, Union[Repository, Directory]] = dict()
    calls: Set[Tuple[str, str]] = set()

    def __init__(self, uri, user, password, database, prune=False, summarize=False) -> None:
        self.repograph = Repograph(uri, user, password, database)

        self.summarize = summarize

        if summarize:
            self.function_summarizer = FunctionSummarizer()

        if prune:
            self.repograph.graph.delete_all()

    def _parse_repository(self, path: str) -> Repository:
        """Parses information about the repository, i.e. the root,
        itself.

        Args:
            path (str): The path of the repository.

        Returns:
            Repository: The created Repository node
        """
        repository = Repository(name=path, type="tbc")  # TODO: Implement type.
        self.repograph.add(repository)
        self.directories[repository.name] = repository
        return repository

    def _parse_requirements(self, requirements: Optional[JSONDict], repository: Repository) -> None:
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
                package = Package.create_from_external_dependency(requirement)
                self.repograph.add(package)
                relationship = Requires(repository, package, version=version)
                self.repograph.add(package, relationship)

    def _parse_directory_tree(self, info):
        pass

    def _parse_license(self, licenses: Optional[JSONDict], repository: Repository) -> None:
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
                        text=licenses.get("text", ""),
                        license_type=detected_type,
                        confidence=(float(confidence.strip('%')) / 100)
                    )
                    relationship = LicensedBy(repository, license_node)
                    self.repograph.add(license_node, relationship)

    def _parse_readme(self, info):
        pass

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
                                   i.e the Directory with the path of parent_path.

            Returns:
                None
            """
            parent = self.directories.get(child.parent_path, None)

            if not parent:
                parent = Directory(child.parent_path)
                relationship = Contains(parent, child)
                self.repograph.add(parent, relationship)
                self.directories[parent.path] = parent
                return add_parents_recursively(parent)
            else:
                parent_relationship = Contains(parent, child)
                self.repograph.add(child, parent_relationship)
                return

        # Attempt to get the parent directory from the list of created directories.
        existing_parent = self.directories.get(parent_path, None)
        if existing_parent:
            return existing_parent

        # If it doesn't exist create a new Directory and then call the recursive function.
        new_parent = Directory(parent_path)
        self.repograph.add(new_parent)
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
            if isinstance(self.directories.get(parent, None), Package):
                parts = [get_path_name(directory_path)] + parts
                parent = get_path_parent
            else:
                return ".".join(parts)

        return ".".join(parts)

    def _parse_directory(
        self,
        directory_name: str,
        directory_info: List[JSONDict],
        index: int,
        total: int
    ) -> None:
        """Parse a directory

        Args:
            directory_name (str): The name of the directory.
            directory_info (JSONDict): The directory information.
            index (int): The index of the directory within the repository.
            total (int): The total number of directories within the repository.
        """
        directory_path = strip_file_path_prefix(directory_name)
        log.info("Parsing directory '%s' (%d/%d)", directory_path, index + 1, total)

        # Whether the directory is a Package. We start
        # by assuming that it isn't.
        is_package = False
        modules = []

        # Parse each file within the directory, update is_package
        # with result (whether file is __init__.py), and add to list
        # of Files.
        for file_index, file_info in enumerate(directory_info):
            module = self._parse_module(file_info, file_index, len(directory_info))
            is_package = is_package or module.name == INIT
            modules.append(module)

        # Get the parent directory
        parent = self._get_parent_directory(get_path_parent(directory_path))

        # If an __init__.py was found, create a Package node,
        # otherwise create a Directory node.
        if is_package:
            canonical_name = self._create_canonical_package_name(directory_path)
            directory = Package.create_from_directory(directory_path, canonical_name)
        else:
            directory = Directory(directory_path)

        # Add the list of created directories, the directory node,
        # and the relationship to its parent, to the Repograph.
        self.directories[directory.path] = directory
        relationship = Contains(parent, directory)
        self.repograph.add(parent, relationship)

        # Parse each of the files within the directory.
        for module in modules:
            relationship = Contains(directory, module)
            self.repograph.add(module, relationship)

    def _parse_module(self, file_info: JSONDict, index: int, total: int) -> Module:
        """Parses a Python module with a parent directory.

        Args:
            file_info (JSONDict): The information about the file to parse.
            index (int): The index of the Module within the parent Folder.
            total (int): The total number of Modules within the parent Folder.

        Returns:
            bool: Whether Module is an __init__.py.
        """
        log.info(
            "--> Parsing file `%s` (%d/%d)",
            file_info["file"]["fileNameBase"],
            index + 1,
            total
        )

        module = Module(
            name=file_info["file"]["fileNameBase"],
            path=file_info["file"]["path"],
            extension=file_info["file"]["extension"],
            is_test=file_info.get("is_test", False)
        )

        self._parse_functions_and_methods(file_info.get("functions", {}), module)
        self._parse_classes(file_info.get("classes", {}), module)

        return module

    def _parse_functions_and_methods(
            self,
            functions_info: JSONDict,
            parent: Union[Module, Class],
            methods: bool = False
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
                source_code=source_code,
                ast=ast_string,
                min_line_number=min_lineno,
                max_line_number=max_lineno
            )

            # Add to graph
            self.repograph.add(function)

            # TODO: Call _parse_docstring
            self._parse_docstring(info.get("doc", {}), function)

            # Create HasFunction Relationship
            if methods:
                relationship = HasMethod(parent, function)
            else:
                relationship = HasFunction(parent, function)
            self.repograph.add(relationship)

            # Parse arguments and create Argument nodes
            self._parse_arguments(
                info.get("args", []),
                info.get("annotated_arg_types", {}),
                function
            )

            # Parse return values and create ReturnValue nodes
            self._parse_return_values(
                info.get("returns", []),
                info.get("annotated_return_type", "Any"),
                function
            )

            # Add a call mapping for each call in the call list to a set
            # so call relationships can be created later.
            for call in info.get("calls", []):
                self.calls.add((function.name, call))

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
                min_line_number=min_lineno,
                max_line_number=max_lineno,
            )
            relationship = Contains(parent, class_node)
            self.repograph.add(class_node)
            self.repograph.add(relationship)

            # Parse extends
            self._parse_extends(info.get("extend", []), class_node)

            # Parse docstring
            self._parse_docstring(info.get("doc", {}), class_node)

            # Parse method info inside class if available
            methods_info = info.get("methods", None)
            if methods_info:
                self._parse_functions_and_methods(methods_info, class_node, methods=True)

    def _parse_arguments(
        self,
        args_list: List[str],
        annotated_arg_types: Dict[str, str],
        parent: Function
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

            argument = Argument(name=arg, type=arg_type)
            relationship = HasArgument(parent, argument)
            self.repograph.add(argument, relationship)

    def _parse_return_values(
        self,
        return_values: List[List[str]],
        annotated_type: str,
        parent: Function
    ) -> None:
        """Parse return values from function/method information.

        Args:
            return_values (List[str]): The list of return value names.
            annotated_type (Dict[str, str]): The annotated return value types.
            parent (Function): The parent function the return values belong to.
        """
        if len(return_values) > 1:
            return_type = "Any"
            # TODO: SH-16 Regex extraction?
        elif len(return_values) == 1:
            return_type = annotated_type
        else:
            return

        # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
        for arg in set([item for sublist in return_values for item in sublist]):
            return_value = ReturnValue(name=arg, type=return_type)
            relationship = Returns(parent, return_value)
            self.repograph.add(return_value, relationship)

    def _parse_docstring(
        self,
        docstring_info: Optional[JSONDict],
        parent: Union[Function, Class]
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
        if (isinstance(parent, Class)):
            if (not docstring_info):
                log.debug(f"No docstring information for class {parent.name}")
                return
        elif (isinstance(parent, Function)):
            if (not docstring_info and not self.summarize):
                log.debug(f"No docstring information for {parent.name}")
                return
        else:
            return

        # Initialise empty arrays for storing created nodes/reationships
        nodes = []
        relationships = []

        summary = self.function_summarizer.summarize_function(parent) if self.summarize else None

        # Parse docstring description
        docstring = Docstring(
            summarization=summary,
            short_description=docstring_info.get("short_description", None),
            long_description=docstring_info.get("long_description", None)
        )
        relationship = Documents(docstring, parent)
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
                    default=arg_info.get("default", None)
                )
                relationship = Describes(docstring, docstring_arg)
                nodes.append(docstring_arg)
                relationships.append(relationship)

            if "returns" in docstring_info:
                # Parse docstring return values
                returns_info = docstring_info.get("returns", {})
                docstring_return_value = DocstringReturnValue(
                    name=returns_info.get("return_name", None),
                    description=returns_info.get("description", None),
                    type=returns_info.get("type_name", None),
                    is_generator=returns_info.get("is_generator", False)
                )
                relationship = Describes(docstring, docstring_return_value)
                nodes.append(docstring_return_value)
                relationships.append(relationship)

            # Parse docstring raises
            for raises in docstring_info.get("raises", []):
                docstring_raises = DocstringRaises(
                    description=raises.get("description", None),
                    type=raises.get("type_name", None)
                )
                relationship = Describes(docstring, docstring_raises)
                nodes.append(docstring_raises)
                relationships.append(relationship)

        # Add nodes and relationships to graph
        self.repograph.add(*nodes, *relationships)

    def _parse_extends(self, extends_info: List[str], class_node: Class) -> None:
        """Parse extends/super class information for a Class node.

        Args:
            extends_info (List[str]): The names of Classes that the Class node extends.
            class_node (Class): The Class node itself.

        Returns:
            None
        """
        if len(extends_info) == 0:
            log.debug("Class `%s` doesn't not extend any other classes", class_node.name)
            return

        for extends in extends_info:
            super_class = Class(name=extends)
            relationship = Extends(class_node, super_class)
            self.repograph.add(super_class, relationship)

    def build(self, directory_info: Dict[str, any]) -> Repograph:
        log.info("Building Repograph...")

        # Pop off non-directory entries from the JSON, for parsing later
        requirements = directory_info.pop("requirements", None)
        _ = directory_info.pop("directory_tree", None)
        licenses = directory_info.pop("license", None)
        _ = directory_info.pop("readme_files", None)

        # Create a sorted list of directory paths.py, as dictionaries are not
        # always sortable in Python.
        log.info("Sorting directories with hierarchical ordering...")
        directories = sorted(
            list(directory_info.keys()),
            key=lambda file: (os.path.dirname(file), os.path.basename(file)))

        # Parse repository root folder if it exists, otherwise manually create
        # the repository node.
        path = strip_file_path_prefix(directories[0])
        if is_root_folder(path):
            repository = self._parse_repository(path)
            directories.pop(0)
        else:
            repository = self._parse_repository(get_path_root(path))

        # Parse requirements
        self._parse_requirements(requirements, repository)

        # Parse license
        self._parse_license(licenses, repository)

        # Parse each directory
        log.info("Extracting information from directories...")
        for index, directory in enumerate(directories):
            self._parse_directory(directory, directory_info[directory], index, len(directories))

        log.info("Successfully built a Repograph!")
        return self.repograph
