"""
Utility functions.
"""
import json
from pathlib import PurePath
from typing import Any, Dict

def read_json_from_file(file_path: str) -> Dict[str, Any]:
  """Reads a JSON object from a file.

  Args:
      file_path (str): The path of the file to read.

  Returns:
      Dict[str, Any]: The JSON object as a dictiontary.
  """
  with open(file_path, "r") as file:
    json_obj = json.load(file)
    return json_obj
  
def strip_file_path_prefix(file_path: str) -> str:
  pure_path = PurePath(file_path)
  pure_path = PurePath("/".join(pure_path.parts[1:]))
  return 