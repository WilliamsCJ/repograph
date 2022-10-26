"""
RepographBuilder generates a populated Repograph from inspect4py JSON output.
"""
import os
from typing import Dict, Union

from repograph.repograph import Repograph
from repograph.models.nodes import Class, Folder, File, Repository
from repograph.models.relationships import Contains
import repograph.utils as utils

ADDITIONAL_KEYS = [
  "requirements",
  "directory_tree",
  "license",
  "readme_files"
]


class RepographBuilder:
    repograph: Repograph
    folders: Dict[str, Union[Repository, Folder]] = {}

    def __init__(self, uri, user, password, database, prune=False) -> None:
        self.repograph = Repograph(uri, user, password, database)

        if prune:
            self.repograph.graph.delete_all()

    def _parse_repository(self, path):
        repository = Repository(path, "type")
        self.repograph.add(repository)
        self.folders[repository.name] = repository

    def _parse_repository_info(self, name, type):
        pass

    def _parse_requirements(self, info):
        pass

    def _parse_directory_tree(self, info):
        pass

    def _parse_license(self, info):
        pass

    def _parse_readme(self, info):
        pass

    def _add_parent_relationship(self, child) -> Folder:
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

    def _parse_directory(self, directory_name, directory_info):
        directory_path = utils.strip_file_path_prefix(directory_name)
        folder = Folder(directory_path)

        self._add_parent_relationship(folder)
        self.folders[folder.path] = folder

        for file_info in directory_info:
            file = File(
                file_info["file"]["fileNameBase"],
                file_info["file"]["path"],
                file_info["file"]["extension"]
            )
            relationship = Contains(folder, file)
            self.repograph.add(file)
            self.repograph.add(relationship)

            self._parse_classes(file_info.get("classes", {}), file)

    def _parse_classes(self, class_info: Dict, parent: File):
        """Parses class information into Class nodes and
        adds links to parent File node.

        Args:
            class_info (Dict): Dictionary containing class information.
            parent (File): Parent Filen node.
        """
        for name, info in class_info.items():
            classNode = Class(
                name,
                info["min_max_lineno"]["min_lineno"],
                info["min_max_lineno"]["max_lineno"],
                info.get("extend", [])
            )
            relationship = Contains(parent, classNode)
            self.repograph.add(classNode)
            self.repograph.add(relationship)

    def build(self, directory_info: Dict[str, any]) -> Repograph:
        # TODO: Parse requirements to create dependency nodes
        self._parse_requirements(directory_info.pop("requirements", None))

        # TODO: Parse directory for an unknown reason
        self._parse_directory_tree(directory_info.pop("directory_tree", None))

        # TODO: Create license node
        self._parse_license(directory_info.pop("license", None))

        # TODO: Create readme nodes
        self._parse_readme(directory_info.pop("readme_files", None))

        # Create a sorted list of directory paths, as dictionaries are not
        # always sortable in Python.
        directories = sorted(
            list(directory_info.keys()),
            key=lambda file: (os.path.dirname(file), os.path.basename(file)))

        # Parse repository root folder if it exists, otherwise manually create
        # the repository node.
        path = utils.strip_file_path_prefix(directories[0])
        print(path)
        if utils.is_root_folder(path):
            self._parse_repository(path)
            directories.pop(0)
        else:
            self._parse_repository(utils.get_path_root(path))

        for directory in directories:
            self._parse_directory(directory, directory_info[directory])

        # TODO: Calculate name and package
        self._parse_repository_info("test", "package")
