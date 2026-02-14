import pathlib
import subprocess
from typing import Tuple
from langchain_core.tools import tool


PROJECT_ROOT = pathlib.Path(__file__).parent.parent / "generated_project"

def project_path(path: str) -> pathlib.Path:
    p = (PROJECT_ROOT / path).resolve()

    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError(f"Invalid path: {path}. Path must be within the project directory.")
    return p


@tool
def write_file(path: str, content: str) -> str:
    """Write a file into the generated project directory.

    Args:
        path: Relative path (from project root) where the file should be written.
        content: File content to write as UTF-8.

    Returns:
        A confirmation string containing the absolute path written.
    """
    p = project_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {p}"


@tool
def read_file(path: str) -> str:
    """Read a file from the generated project directory and return its content.

    Args:
        path: Relative path (from project root) of the file to read.

    Returns:
        The file content as a string, or an error message if the file is missing.
    """
    p = project_path(path)
    if not p.exists():
        return f"File not found: {p}"
    with open(p, "r", encoding="utf-8") as f:
        return f.read()

@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = project_path(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = project_path(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)