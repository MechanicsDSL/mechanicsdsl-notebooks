"""
_cli.py
-------
CLI and utility functions for mechanicsdsl-notebooks.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import subprocess
import sys


_NOTEBOOKS = {
    "01_double_pendulum":    "01_double_pendulum.ipynb",
    "02_coupled_oscillators": "02_coupled_oscillators.ipynb",
    "03_constraints":        "03_constraints.ipynb",
    "04_central_forces":     "04_central_forces.ipynb",
    "05_hamiltonian":        "05_hamiltonian.ipynb",
}


def list_notebooks() -> List[str]:
    """Return names of all available notebooks."""
    return sorted(_NOTEBOOKS.keys())


def get_notebook_path(name: str) -> Optional[Path]:
    """
    Return the path to a notebook by name.

    Parameters
    ----------
    name : str
        Notebook name. Use list_notebooks() to see available options.

    Returns
    -------
    Path or None
    """
    if name not in _NOTEBOOKS:
        raise ValueError(f"Unknown notebook '{name}'. Available: {list_notebooks()}")
    pkg_dir = Path(__file__).parent
    nb_dir = pkg_dir / "notebooks"
    if nb_dir.exists():
        return nb_dir / _NOTEBOOKS[name]
    # Local clone
    repo_root = pkg_dir.parent.parent.parent.parent
    local = repo_root / "notebooks" / _NOTEBOOKS[name]
    if local.exists():
        return local
    return None


def main() -> None:
    """Entry point for mechanicsdsl-notebooks CLI."""
    import argparse
    parser = argparse.ArgumentParser(
        prog="mechanicsdsl-notebooks",
        description="MechanicsDSL Jupyter notebooks"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List available notebooks")
    launch_p = sub.add_parser("launch", help="Launch Jupyter Lab")
    launch_p.add_argument("--notebook", "-n", default=None, help="Open specific notebook")

    args = parser.parse_args()

    if args.command == "list":
        print("Available MechanicsDSL notebooks:")
        for nb in list_notebooks():
            print(f"  {nb}")

    elif args.command == "launch":
        cmd = ["jupyter", "lab"]
        if args.notebook:
            path = get_notebook_path(args.notebook)
            if path:
                cmd.append(str(path))
            else:
                print(f"Notebook '{args.notebook}' not found locally. "
                      f"Try: pip install mechanicsdsl-notebooks[notebooks]")
                sys.exit(1)
        subprocess.run(cmd)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
