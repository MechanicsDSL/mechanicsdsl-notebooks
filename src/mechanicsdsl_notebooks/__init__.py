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

__all__ = ["__version__", "list_notebooks", "get_notebook_path"]
