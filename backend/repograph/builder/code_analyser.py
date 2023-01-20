"""

"""
import logging
import shutil
import subprocess

log = logging.getLogger('repograph.code_analyser')


def call_inspect4py(input_path: str, output_path: str) -> str:
    """Call inspect4py for code analysis and extraction.

    Args:
        input_path (str): The path of the repository
        output_path (str): The path to output inspect4py to.

    Returns:
        output_path (str)
    """
    log.info("Extracting information from %s using inspect4py...", input_path)

    subprocess.check_call([
        "inspect4py",
        "-i",
        input_path,
        "-o",
        output_path,
        "-md",
        "-rm",
        "-si",
        "-ld",
        "-sc",
        "-ast",
    ])

    log.info("Done!")
    return output_path


def cleanup_inspect4py_output() -> None:
    log.info("Cleaning up temporary directory...")
    shutil.rmtree("./tmp")
    log.info("Done!")
