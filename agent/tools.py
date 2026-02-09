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


@tool("write_file")
def write_file(path: str, content: str) -> str:
    p = project_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {p}"


@tool("read_file")
def read_file(path: str) -> str:
    p = project_path(path)
    if not p.exists():
        return f"File not found: {p}"
    with open(p, "r", encoding="utf-8") as f:
        return f.read()