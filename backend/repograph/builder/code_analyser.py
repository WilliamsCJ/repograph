"""

"""
import logging
import shutil
import subprocess

log = logging.getLogger('repograph.code_analyser')


def call_inspect4py(input_path: str, output_path: str) -> str:
    """

    Args:
        repository_path:
        repository_name:

    Returns:

    """
    log.info("Extracting information from %s using inspect4py...", input_path)

    subprocess.run([
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
        "-ast"
    ])

    log.info("Done!")
    return output_path


def cleanup_inspect4py_output(output_path: str) -> None:
    log.info("Cleaning up temporary directory...")
    shutil.rmtree(output_path)
    log.info("Done!")
