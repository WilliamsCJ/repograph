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
from repograph.models.relationships import Contains, Describes, Documents, HasArgument, \
                                           HasFunction, HasMethod, ImportedBy, LicensedBy, \
                                           Returns, Requires
from repograph.utils.json import JSONDict, parse_min_max_line_numbers, \
    marshall_json_to_string
from repograph.utils.paths import strip_file_path_prefix, is_root_folder, get_path_name, \
                                  get_path_root, get_path_parent, get_package_parent_and_name

ADDITIONAL_KEYS = [
  "requirements",
  "directory_tree",
  "license",
  "readme_files"
]

INIT = "__init__"

log = logging.getLogger('repograph.repograph_builder')


class RepographBuilder:
    """
    Generates a Repograph from inspect4py output.
    """

    # The Repograph object used to read/write to the graph
    repograph: Repograph

    # The function summarizer function
    function_summarizer: FunctionSummarizer

    # Summarization flag
    summarize: bool

    # Mapping of paths to Directory (or the Repository) object
    directories: Dict[str, Union[Repository, Directory]] = dict()

    # Mapping of paths/pacakge names to modules
    modules: Dict[str, Module] = dict()

    # Mapping of Module objects to Classes/Function objects
    module_objects: Dict[Module, List[Union[Class, Function]]] = dict()

    # Mapping Module dependencies for retrospective parsing
    module_dependencies: List[Tuple[List[JSONDict], Module]] = []

    # Packages from requirements file
    requirements: Dict[str, Package] = dict()

    # TODO:
    calls: Set[Tuple[str, str]] = set()

    def __init__(self, uri, user, password, database, prune=False, summarize=False) -> None:
        """Constructor

        Args:
            uri:
            user:
            password:
            database:
            prune:
            summarize:
        """
        self.repograph = Repograph(uri, user, password, database)

        self.summarize = summarize

        if summarize:
            self.function_summarizer = FunctionSummarizer()

        if prune:
            self.repograph.graph.delete_all()

    def _parse_repository(self, path: str, directory_info: List[JSONDict] = None) -> Repository:
        """Parses information about the repository, i.e. the root,
        itself.

        Args:
            path (str): The path of the repository.

        Returns:
            Repository: The created Repository node
        """
        is_package = False
        modules = []

        # Parse files within this folder, as Python files may be contained in the repository root
        if directory_info:
            modules, is_package = self._parse_files_in_directory(directory_info)

        # TODO: Implement type.
        repository = Repository(name=path, type="tbc", is_root_package=is_package)
        self.repograph.add(repository)
        self.directories[repository.name] = repository

        # Parse each extracted module
        for module, file_info in modules:
            # If repository root is a package, add the full canonical name as such
            if repository.is_root_package:
                module = module.update_canonical_name(f"{repository.name}.{module.name}")

            # Now parse the contents of the  module
            self._parse_module_contents(module, file_info)

            # Create a relationship between the Repository and the Module
            relationship = Contains(repository, module)
            self.repograph.add(module, relationship)

            # Finally add the module to the list of stored modules
            self.modules[module.canonical_name] = module
            self.modules[module.path] = module

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
                self.requirements[requirement] = package

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
                                   i.e. the Directory with the path of parent_path.

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
            parent_node = self.directories.get(parent, None)

            if isinstance(parent_node, Package) or (isinstance(parent_node, Repository) and parent_node.is_root_package):  # noqa: 501
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
            directory = Package.create_from_directory(directory_path, canonical_name)
        else:
            directory = Directory(directory_path)

        # Add the list of created directories, the directory node,
        # and the relationship to its parent, to the Repograph.
        self.directories[directory.path] = directory
        relationship = Contains(parent, directory)
        self.repograph.add(parent, relationship)

        # Parse each extracted module
        for module, file_info in modules:
            # If parent is a package, add the full canonical path name and add to modules.
            if isinstance(directory, Package):
                module = module.update_canonical_name(f"{directory.canonical_name}.{module.name}")
                self.modules[module.canonical_name] = module

            # Now parse the contents of the module.
            self._parse_module_contents(module, file_info)

            # Create a relationship between the Directory and the Module.
            relationship = Contains(directory, module)
            self.repograph.add(module, relationship)

            # Finally add the module to the list of stored modules.
            self.modules[module.path] = module
            self.modules[module.canonical_name] = module

    def _parse_files_in_directory(self, directory_info: List[JSONDict]) -> Tuple[List[Tuple[Module, JSONDict]], bool]:  # noqa: 501
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
        log.info(
            "--> Parsing file `%s` (%d/%d)",
            file_info["file"]["fileNameBase"],
            index + 1,
            total
        )

        module = Module(
            name=file_info["file"]["fileNameBase"],
            canonical_name=file_info["file"]["fileNameBase"],
            path=file_info["file"]["path"],
            parent_path=get_path_parent(file_info["file"]["path"]),
            extension=file_info["file"]["extension"],
            is_test=file_info.get("is_test", False)
        )

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
            self.module_dependencies.append((file_info.get("dependencies", []), module))

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

            # Parse the docstring for the function
            self._parse_docstring(info.get("doc", {}), function)

            # Create HasFunction Relationship
            if methods:
                relationship = HasMethod(parent, function)
            else:
                relationship = HasFunction(parent, function)
            self.repograph.add(relationship)

            # If parent is a module, add to the module_objects set
            if isinstance(parent, Module):
                self.module_objects[parent] = self.module_objects.get(parent, []) + [function]

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

            # Add to module objects set
            self.module_objects[parent] = self.module_objects.get(parent, []) + [class_node]

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

        def parse(values):
            for value in values:
                if isinstance(value, list):
                    parse(value)
                elif isinstance(value, str):
                    return_value = ReturnValue(name=value, type=return_type)
                    relationship = Returns(parent, return_value)
                    self.repograph.add(return_value, relationship)
                else:
                    log.error(
                        "Unexpected return value type `%s` for function `%s`",
                        type(value),
                        parent.name
                    )

        parse(return_values)

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
        if isinstance(parent, Class):
            if not docstring_info:
                log.debug(f"No docstring information for class {parent.name}")
                return
        elif isinstance(parent, Function):
            if not docstring_info and not self.summarize:
                log.debug(f"No docstring information for {parent.name}")
                return
        else:
            return

        # Initialise empty arrays for storing created nodes/relationships
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

    def _parse_dependencies(self) -> None:
        """Parse the dependencies between Modules.

        Returns:
            None
        """
        # Iterate through dependencies for each required module
        for dependency_info, module in self.module_dependencies:
            # Iterate through each dependency in the module
            for dependency in dependency_info:
                log.info(f"Module: {module.name}")
                log.info("Dependency:")
                log.info(dependency)
                # Check whether a module object or module itself is being imported
                if "from_module" in dependency:
                    imports_module = False
                else:
                    imports_module = True

                print(dependency)

                # Get the imported object (either module or object)
                imported_object = dependency["import"]
                source_module = dependency.get("from_module", imported_object)

                # Find the module
                if dependency["type"] == "internal":
                    imported_module = self.modules.get(
                        f"{module.parent_path}/{source_module}.py",
                        None
                    )
                else:
                    imported_module = self.modules.get(source_module, None)

                # If importing a module directly....
                if imports_module:
                    # ...and it already exists create the relationship
                    if imported_module:
                        self.repograph.add(ImportedBy(imported_module, module))
                    # ...and if it doesn't recursively create it
                    else:
                        source_module, missing = self._calculate_missing_packages(source_module)

                        if source_module == "":
                            self._create_missing_nodes(missing)
                        elif source_module in self.requirements:
                            self._create_missing_nodes(
                                missing,
                                parent=self.requirements[source_module]
                            )
                        else:
                            self._create_missing_nodes(
                                missing,
                                parent=self.modules[source_module]
                            )
                # If importing a class, function, etc...
                else:
                    # ...and it already exists create the relationship
                    if imported_module:
                        module_objects = self.module_objects.get(imported_module, None)
                        if not module_objects:
                            log.warning("Module provides no objects")
                            continue

                        # Filter the module objects for only those with the imported name
                        matching_objects = [obj for obj in module_objects if obj.name == imported_object]  # noqa: 501

                        # If no matches, log an error and move onto the next dependency
                        if len(matching_objects) == 0:
                            log.error("No matching objects")
                            continue

                        # If more than one match we log this inconsistency,
                        # but add all import relationships
                        if len(matching_objects) > 1:
                            log.warning("More than 1 matching object found in import.")

                        for match in matching_objects:
                            self.repograph.add(ImportedBy(match, module))
                    # ...and if it doesn't recursively create it
                    else:
                        if imported_object[0].isupper():
                            imported_object = Class(name=imported_object)
                        else:
                            imported_object = Function(
                                name=imported_object,
                                type=str(Function.FunctionType.FUNCTION.value)
                            )

                        source_module, missing = self._calculate_missing_packages(source_module)

                        if source_module == "":
                            self._create_missing_nodes(missing)
                        elif source_module in self.requirements:
                            self._create_missing_nodes(
                                missing,
                                parent=self.requirements[source_module],
                                import_object=imported_object
                            )
                        else:
                            self._create_missing_nodes(
                                missing,
                                parent=self.modules[source_module],
                                import_object=imported_object
                            )

                        self.repograph.add(ImportedBy(imported_object, module))

    def _calculate_missing_packages(self, source_module) -> Tuple[str, List[str]]:
        missing = []
        while source_module not in self.modules and source_module not in self.requirements and source_module != "":  # noqa: 501
            parent, child = get_package_parent_and_name(source_module)
            missing.append(child)
            source_module = parent

        return source_module, missing

    def _create_missing_nodes(
            self,
            missing: List[str],
            parent: Package = None,
            import_object: Union[Class, Function] = None
    ) -> Tuple[List[Package], List[Contains]]:
        nodes = []
        relationships = []

        max = len(missing) - 1
        for index, m in enumerate(missing):
            if index == max:
                new = Module(name=m)
            else:
                new = Package(
                    name=m,
                    canonical_name=f"{parent.canonical_name}.{m}" if parent else m,
                    parent_package=parent.canonical_name if parent else "",
                    external=True
                )

            if parent:
                relationships.append(Contains(parent, new))

            parent = new
            nodes.append(new)

        # If we have an import_object, but the parent is a Package, create an __init__ Module
        # as this is actually where the import_object is being imported from.
        if import_object and parent and isinstance(parent, Package):
            new = Module.create_init_module(parent.canonical_name)
            relationships.append(Contains(parent, new))
            parent = new

        # If we have an import object, create a Contains relationship with the parent module.
        if import_object:
            relationships.append(Contains(parent, import_object))

        # Add the created nodes and relationships to the Repograph.
        self.repograph.add(*nodes, *relationships)

        return nodes, relationships

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

        # TODO: Implement Extends properly
        # for extends in extends_info:
        #     super_class = Class(name=extends)
        #     relationship = Extends(class_node, super_class)
        #     self.repograph.add(super_class, relationship)

    def build(self, directory_info: JSONDict) -> Repograph:
        """Build a repograph from directory_info JSON.

        Args:
            directory_info (JSONDict): Directory info JSON.

        Returns:
            Repograph
        """
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
            directory = directories.pop(0)
            repository = self._parse_repository(path, directory_info[directory])
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

        # Retrospectively parse module dependencies
        log.info("Parsing module dependencies...")
        self._parse_dependencies()

        log.info("Successfully built a Repograph!")
        return self.repograph
