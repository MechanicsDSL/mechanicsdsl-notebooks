"""
mechanicsdsl-notebooks
----------------------
Curated Jupyter notebooks for MechanicsDSL spanning all eight physics domains.

Quick start:
    # Launch locally
    pip install mechanicsdsl-notebooks
    mechanicsdsl-notebooks launch

    # Or browse notebooks directly at:
    # https://github.com/MechanicsDSL/mechanicsdsl-notebooks
    # https://mybinder.org/v2/gh/MechanicsDSL/mechanicsdsl-notebooks/main
"""

from mechanicsdsl_notebooks._version import __version__
from mechanicsdsl_notebooks._cli import list_notebooks, get_notebook_path
from mechanicsdsl_notebooks._bridge import (
    CompiledSystem,
    CoreNotInstalled,
    DSLCompileError,
    compile_spec,
)
from mechanicsdsl_notebooks._generate import build_notebook, code_cell_sources

__all__ = [
    "__version__",
    "list_notebooks",
    "get_notebook_path",
    "compile_spec",
    "build_notebook",
    "code_cell_sources",
    "CompiledSystem",
    "CoreNotInstalled",
    "DSLCompileError",
]
