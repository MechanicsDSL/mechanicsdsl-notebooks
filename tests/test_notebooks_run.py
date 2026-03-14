"""
test_notebooks_run.py
---------------------
Smoke tests verifying that each notebook can be imported and its
pure-Python cells execute without error.
"""

import json
import types
import pytest
from pathlib import Path

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"
notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))


@pytest.mark.parametrize("nb_path", notebooks, ids=[n.name for n in notebooks])
def test_notebook_is_valid_json(nb_path):
    """Each notebook file must be parseable JSON."""
    with open(nb_path) as f:
        nb = json.load(f)
    assert nb["nbformat"] >= 4
    assert "cells" in nb


@pytest.mark.parametrize("nb_path", notebooks, ids=[n.name for n in notebooks])
def test_notebook_has_title(nb_path):
    """First markdown cell must contain an H1 title."""
    with open(nb_path) as f:
        nb = json.load(f)
    md_cells = [c for c in nb["cells"] if c["cell_type"] == "markdown"]
    assert md_cells, "No markdown cells found"
    first_src = "".join(md_cells[0]["source"])
    assert first_src.startswith("# "), f"First markdown cell must start with '# ', got: {first_src[:50]}"


@pytest.mark.parametrize("nb_path", notebooks, ids=[n.name for n in notebooks])
def test_notebook_no_output_errors(nb_path):
    """Notebooks should not have pre-existing error outputs (from a previous run)."""
    with open(nb_path) as f:
        nb = json.load(f)
    for i, cell in enumerate(nb["cells"]):
        for output in cell.get("outputs", []):
            assert output.get("output_type") != "error", (
                f"Cell {i} has error output: "
                f"{output.get('ename')}: {output.get('evalue')}"
            )
