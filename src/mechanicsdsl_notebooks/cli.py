"""
cli.py
------
Command-line interface for ``mechanicsdsl-notebooks``.

Lists and launches the curated notebooks, and *generates* fresh, runnable
notebooks from any DSL spec or preset, optionally executed so they ship with
outputs already in them.

Usage
-----
    mechanicsdsl-notebooks list
    mechanicsdsl-notebooks presets
    mechanicsdsl-notebooks generate double_pendulum -o notebooks/
    mechanicsdsl-notebooks generate double_pendulum --sections all --execute -o notebooks/
    mechanicsdsl-notebooks generate kepler --sections phase,energy --duration 3.2e7
    mechanicsdsl-notebooks build-all --execute -o gallery/
    mechanicsdsl-notebooks check notebooks/01_double_pendulum.ipynb
    mechanicsdsl-notebooks launch --notebook 01_double_pendulum
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import List, Optional

from ._bridge import CoreNotInstalled, DSLCompileError, compile_spec, list_presets
from ._cli import get_notebook_path, list_notebooks
from ._execute import NotebookExecutionError, execute_notebook
from ._generate import SECTIONS, build_notebook


def _parse_sections(text: str) -> List[str]:
    if text == "all":
        return list(SECTIONS)
    parts = [s.strip() for s in text.split(",") if s.strip()]
    bad = [p for p in parts if p not in SECTIONS]
    if bad:
        raise argparse.ArgumentTypeError(
            f"unknown section(s) {bad}; choose from {', '.join(SECTIONS)} or 'all'")
    return parts


def _write_nb(nb: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(nb, fh, indent=1)
        fh.write("\n")


def _list(_: argparse.Namespace) -> int:
    print("Available MechanicsDSL notebooks:")
    for nb in list_notebooks():
        print(f"  {nb}")
    return 0


def _presets(_: argparse.Namespace) -> int:
    print("Presets shipped with mechanicsdsl-core:")
    for name in list_presets():
        print(f"  {name}")
    return 0


def _make(spec: str, args: argparse.Namespace):
    system = compile_spec(spec)
    nb = build_notebook(system, duration=args.duration, num_points=args.points,
                        sections=args.sections, sweep_parameter=args.sweep)
    if args.execute:
        nb, _ = execute_notebook(nb)
    return system, nb


def _generate(args: argparse.Namespace) -> int:
    try:
        system, nb = _make(args.spec, args)
    except CoreNotInstalled as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except DSLCompileError as exc:
        print(f"DSL compilation failed: {exc}", file=sys.stderr)
        return 1
    except NotebookExecutionError as exc:
        print(f"Generated notebook failed to execute: {exc}", file=sys.stderr)
        return 4
    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, f"{system.name}.ipynb")
    _write_nb(nb, out_path)
    state = "executed" if args.execute else "unexecuted"
    print(f"Compiled '{system.name}' ({system.dof} DOF) -> {out_path} ({state})")
    return 0


def _build_all(args: argparse.Namespace) -> int:
    os.makedirs(args.out, exist_ok=True)
    seen, rows, failures = set(), [], 0
    for preset in list_presets():
        try:
            system, nb = _make(preset, args)
        except (DSLCompileError, NotebookExecutionError) as exc:
            print(f"  {preset}: FAILED ({exc})", file=sys.stderr)
            failures += 1
            continue
        if system.name in seen:  # several preset aliases compile to one system
            continue
        seen.add(system.name)
        name = f"{system.name}.ipynb"
        _write_nb(nb, os.path.join(args.out, name))
        rows.append(f"| [{system.name}]({name}) | {system.dof} | "
                    f"{', '.join(system.coordinates)} | "
                    f"{'yes' if system.conservative else 'no'} |")
        print(f"  {system.name} -> {name}")
    index = ["# Generated notebook gallery", "",
             "Built by `mechanicsdsl-notebooks build-all` from every core preset.", "",
             f"Sections: {', '.join(args.sections) or 'overview'}", "",
             "| System | DOF | Coordinates | Conservative |", "|---|---|---|---|", *rows, ""]
    with open(os.path.join(args.out, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(index))
    print(f"Wrote {len(rows)} notebooks and README.md to {args.out}")
    return 1 if failures else 0


def _check(args: argparse.Namespace) -> int:
    bad = 0
    for path in args.notebooks:
        if not os.path.isfile(path):
            resolved = get_notebook_path(path) if path in list_notebooks() else None
            if resolved is None:
                print(f"  {path}: not found", file=sys.stderr)
                bad += 1
                continue
            path = str(resolved)
        with open(path, encoding="utf-8") as fh:
            nb = json.load(fh)
        executed, _ = execute_notebook(nb, allow_errors=True)
        errors = [o for c in executed["cells"] for o in c.get("outputs", [])
                  if o.get("output_type") == "error"]
        if errors:
            bad += 1
            print(f"  FAIL {path}: {errors[0]['ename']}: {errors[0]['evalue']}")
        else:
            print(f"  ok   {path}")
        if args.write:
            _write_nb(executed, path)
    return 1 if bad else 0


def _launch(args: argparse.Namespace) -> int:
    cmd = ["jupyter", "lab"]
    if args.notebook:
        path = get_notebook_path(args.notebook)
        if path is None:
            print(f"Notebook '{args.notebook}' not found locally. "
                  "Clone the repository to get the curated notebooks.", file=sys.stderr)
            return 1
        cmd.append(str(path))
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError:
        print("Jupyter is not installed. Install with: pip install jupyterlab", file=sys.stderr)
        return 1


def _add_gen_options(p: argparse.ArgumentParser) -> None:
    p.add_argument("--out", "-o", default=".", help="Output directory")
    p.add_argument("--duration", type=float, default=10.0, help="Simulation duration [s]")
    p.add_argument("--points", type=int, default=1000, help="Number of samples")
    p.add_argument("--sections", type=_parse_sections, default=["overview"],
                   help=f"Comma-separated sections ({', '.join(SECTIONS)}) or 'all'")
    p.add_argument("--sweep", default=None, help="Parameter for the 'sweep' section")
    p.add_argument("--execute", action="store_true",
                   help="Run the notebook headlessly and store its outputs")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mechanicsdsl-notebooks",
        description="Curated and generated Jupyter notebooks for MechanicsDSL.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List curated notebooks").set_defaults(func=_list)
    sub.add_parser("presets", help="List core presets").set_defaults(func=_presets)

    p_gen = sub.add_parser("generate", help="Generate a notebook from a DSL spec")
    p_gen.add_argument("spec", help="Path to a .msl file, a raw DSL string, or a preset name.")
    _add_gen_options(p_gen)
    p_gen.set_defaults(func=_generate)

    p_all = sub.add_parser("build-all", help="Generate a notebook for every core preset")
    _add_gen_options(p_all)
    p_all.set_defaults(func=_build_all)

    p_chk = sub.add_parser("check", help="Execute notebooks headlessly and report errors")
    p_chk.add_argument("notebooks", nargs="+", help="Notebook paths or curated names")
    p_chk.add_argument("--write", action="store_true", help="Save outputs back into the files")
    p_chk.set_defaults(func=_check)

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
