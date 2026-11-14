"""
cli.py
------
Command-line interface for ``mechanicsdsl-notebooks``.

This module is the entry point referenced by ``pyproject.toml``
(``mechanicsdsl_notebooks.cli:main``). In addition to listing and launching
the curated notebooks, it can *generate* a fresh, runnable notebook from any
DSL spec or preset.

Usage
-----
    mechanicsdsl-notebooks list
    mechanicsdsl-notebooks generate double_pendulum -o notebooks/
    mechanicsdsl-notebooks launch --notebook 01_double_pendulum
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

from ._bridge import CoreNotInstalled, DSLCompileError, compile_spec
from ._cli import get_notebook_path, list_notebooks
from ._generate import build_notebook


def _list(_: argparse.Namespace) -> int:
    print("Available MechanicsDSL notebooks:")
    for nb in list_notebooks():
        print(f"  {nb}")
    return 0


def _generate(args: argparse.Namespace) -> int:
    try:
        system = compile_spec(args.spec)
    except CoreNotInstalled as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except DSLCompileError as exc:
        print(f"DSL compilation failed: {exc}", file=sys.stderr)
        return 1

    nb = build_notebook(system, duration=args.duration, num_points=args.points)
    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, f"{system.name}.ipynb")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(nb, fh, indent=1)
        fh.write("\n")
    print(
        f"Compiled '{system.name}' "
        f"({len(system.coordinates)} DOF) -> {out_path}"
    )
    return 0


def _launch(args: argparse.Namespace) -> int:
    cmd = ["jupyter", "lab"]
    if args.notebook:
        path = get_notebook_path(args.notebook)
        if path is None:
            print(
                f"Notebook '{args.notebook}' not found locally. "
                "Try: pip install mechanicsdsl-notebooks[notebooks]",
                file=sys.stderr,
            )
            return 1
        cmd.append(str(path))
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError:
        print("Jupyter is not installed. Install with: "
              "pip install mechanicsdsl-notebooks[notebooks]", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mechanicsdsl-notebooks",
        description="Curated and generated Jupyter notebooks for MechanicsDSL.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List curated notebooks").set_defaults(func=_list)

    p_gen = sub.add_parser("generate", help="Generate a notebook from a DSL spec")
    p_gen.add_argument(
        "spec",
        help="Path to a .msl file, a raw DSL string, or a core preset name.",
    )
    p_gen.add_argument("--out", "-o", default=".", help="Output directory")
    p_gen.add_argument("--duration", type=float, default=10.0,
                       help="Simulation duration [s]")
    p_gen.add_argument("--points", type=int, default=1000,
                       help="Number of samples")
    p_gen.set_defaults(func=_generate)

    p_launch = sub.add_parser("launch", help="Launch Jupyter Lab")
    p_launch.add_argument("--notebook", "-n", default=None,
                          help="Open a specific curated notebook")
    p_launch.set_defaults(func=_launch)
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
