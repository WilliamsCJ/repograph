"""
RepographBuilder generates a populated Repograph from inspect4py JSON output.
"""
import logging
import os
from typing import Dict, Set, List, Optional, Tuple, Union

from repograph.repograph import Repograph
from repograph.models.nodes import Argument, Class, Folder, File, \
                                   Function, License, Package, Repository, ReturnValue
from repograph.models.relationships import Contains, HasArgument, HasFunction, \
                                           HasMethod, LicensedBy, Returns, Requires
import repograph.utils as utils
from repograph.utils import JSONDict


ADDITIONAL_KEYS = [
  "requirements",
  "directory_tree",
  "license",
  "readme_files"
]

log = logging.getLogger('repograph.repograph_builder')


class RepographBuilder:
    repograph: Repograph
    summarize: bool
    folders: Dict[str, Union[Repository, Folder]] = dict()
    calls: Set[Tuple[str, str]] = set()

    def __init__(self, uri, user, password, database, prune=False, summarize=False) -> None:
        from repograph.function_summarizer import FunctionSummarizer

        self.repograph = Repograph(uri, user, password, database)
        self.function_summarizer = FunctionSummarizer()
        self.summarize = summarize

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
        self.folders[repository.name] = repository
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
                package = Package(name=requirement, external=True)
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

    def _add_parent_relationship(self, child) -> Optional[Folder]:
        parent = self.folders.get(child.parent, None)

        if not parent:
            parent = Folder(child.parent)
            relationship = Contains(parent, child)
            self.repograph.add(parent, relationship)
            self.folders[parent.path] = parent
            return self._add_parent_relationship(parent)
        else:
            parent_relationship = Contains(parent, child)
            self.repograph.add(child, parent_relationship)
            return

    def _parse_directory(self, directory_name, directory_info, index, total):
        directory_path = utils.strip_file_path_prefix(directory_name)
        log.info("Parsing directory '%s' (%d/%d)", directory_path, index, total)

        folder = Folder(directory_path)

        self._add_parent_relationship(folder)
        self.folders[folder.path] = folder

        for file_index, file_info in enumerate(directory_info):
            log.info(
                "--> Parsing file `%s` in `%s` (%d/%d)",
                file_info["file"]["fileNameBase"],
                directory_path,
                file_index,
                len(directory_info)
            )

            file = File(
                name=file_info["file"]["fileNameBase"],
                path=file_info["file"]["path"],
                extension=file_info["file"]["extension"],
                is_test=file_info.get("is_test", False)
            )
            relationship = Contains(folder, file)
            self.repograph.add(file)
            self.repograph.add(relationship)

            self._parse_functions_and_methods(file_info.get("functions", {}), file)
            self._parse_classes(file_info.get("classes", {}), file)

    def _parse_functions_and_methods(
            self,
            functions_info: utils.JSONDict,
            parent: Union[File, Class],
            methods: bool = False
    ) -> None:
        """Parses function/method information into Function/Method nodes and adds links
        to the parent File/Class node.

        Args:
            functions_info (utils.JSONDict): JSON dictionary containing the function information.
            parent (Union[File, Class]): Parent File or Class node.
            methods (bool): Whether to create Method nodes rather than Function nodes.
        """
        for name, info in functions_info.items():
            # Get min-max line numbers
            min_lineno, max_lineno = utils.parse_min_max_line_numbers(info)
            if not min_lineno or not max_lineno:
                log.warning("Missing line number information for function '%s'", name)

            # Serialise the AST
            ast = info.get("ast")
            if ast:
                ast_string = utils.marshall_json_to_string(ast)
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

            # If summarization enabled, then generate function summarizations
            if self.summarize:
                docstring, documents = self.function_summarizer.create_docstring_node(function)
                self.repograph.add(docstring, documents)

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

    def _parse_classes(self, class_info: Dict, parent: File) -> None:
        """Parses class information into Class nodes and
        adds links to parent File node.

        Args:
            class_info (Dict): Dictionary containing class information.
            parent (File): Parent File node.
        """
        for name, info in class_info.items():
            min_lineno, max_lineno = utils.parse_min_max_line_numbers(info)
            class_node = Class(
                name=name,
                min_line_number=min_lineno,
                max_line_number=max_lineno,
                extends=info.get("extend", [])
            )
            relationship = Contains(parent, class_node)
            self.repograph.add(class_node)
            self.repograph.add(relationship)

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

    def build(self, directory_info: Dict[str, any]) -> Repograph:
        log.info("Building Repograph...")

        # Pop off non-directory entries from the JSON, for parsing later
        requirements = directory_info.pop("requirements", None)
        _ = directory_info.pop("directory_tree", None)
        licenses = directory_info.pop("license", None)
        _ = directory_info.pop("readme_files", None)

        # Create a sorted list of directory paths, as dictionaries are not
        # always sortable in Python.
        log.info("Sorting directories with hierarchical ordering...")
        directories = sorted(
            list(directory_info.keys()),
            key=lambda file: (os.path.dirname(file), os.path.basename(file)))

        # Parse repository root folder if it exists, otherwise manually create
        # the repository node.
        path = utils.strip_file_path_prefix(directories[0])
        if utils.is_root_folder(path):
            repository = self._parse_repository(path)
            directories.pop(0)
        else:
            repository = self._parse_repository(utils.get_path_root(path))

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
