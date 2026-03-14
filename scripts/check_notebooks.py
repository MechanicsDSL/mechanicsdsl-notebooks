#!/usr/bin/env python3
"""
check_notebooks.py
------------------
Execute all notebooks in the notebooks/ directory and report errors.
Uses nbconvert to run each notebook with a timeout.

Usage:
    python scripts/check_notebooks.py
    python scripts/check_notebooks.py --timeout 600
    python scripts/check_notebooks.py --notebook notebooks/01_double_pendulum.ipynb
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def check_notebook(nb_path: Path, timeout: int = 300) -> tuple[bool, list[str]]:
    """Execute a notebook and return (success, list_of_errors)."""
    with tempfile.NamedTemporaryFile(suffix=".ipynb", delete=False) as tmp:
        tmp_path = tmp.name

    result = subprocess.run(
        [
            sys.executable, "-m", "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            f"--ExecutePreprocessor.timeout={timeout}",
            "--output", tmp_path,
            str(nb_path),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return False, [f"nbconvert failed: {result.stderr[:500]}"]

    # Parse executed notebook for error outputs
    errors = []
    try:
        with open(tmp_path) as f:
            nb = json.load(f)
        for i, cell in enumerate(nb["cells"]):
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    errors.append(
                        f"Cell {i}: {output['ename']}: {output['evalue']}"
                    )
    except Exception as e:
        errors.append(f"Parse error: {e}")

    Path(tmp_path).unlink(missing_ok=True)
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="Execute and validate notebooks")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--notebook", type=str, default=None)
    args = parser.parse_args()

    root = Path(__file__).parent.parent

    if args.notebook:
        notebooks = [Path(args.notebook)]
    else:
        notebooks = sorted((root / "notebooks").glob("*.ipynb"))

    if not notebooks:
        print("No notebooks found.")
        sys.exit(0)

    passed, failed = [], []

    for nb in notebooks:
        print(f"Checking {nb.name}...", end=" ", flush=True)
        success, errors = check_notebook(nb, args.timeout)
        if success:
            print("✓")
            passed.append(nb.name)
        else:
            print("✗")
            for e in errors:
                print(f"  ERROR: {e}")
            failed.append(nb.name)

    print(f"\n{len(passed)} passed, {len(failed)} failed.")
    if failed:
        print("Failed:", failed)
        sys.exit(1)


if __name__ == "__main__":
    main()
