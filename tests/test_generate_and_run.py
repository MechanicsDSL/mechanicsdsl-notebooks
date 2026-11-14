"""
test_generate_and_run.py
------------------------
Verifies that generated notebooks are (a) valid nbformat documents and (b)
actually runnable: the code cells are executed in-process against
``mechanicsdsl-core``, so a broken generator or a broken bridge fails CI even
without a Jupyter kernel installed.

Run with: pytest tests/test_generate_and_run.py -v
"""
import matplotlib

matplotlib.use("Agg")  # headless plotting

import pytest

pytest.importorskip(
    "mechanics_dsl", reason="mechanicsdsl-core required for notebook generation"
)

from mechanicsdsl_notebooks import (
    build_notebook,
    code_cell_sources,
    compile_spec,
)


def _run_notebook_code(notebook) -> dict:
    """Execute all code cells in a shared namespace; return that namespace."""
    ns: dict = {}
    for src in code_cell_sources(notebook):
        exec(compile(src, "<cell>", "exec"), ns)  # noqa: S102
    return ns


@pytest.mark.parametrize("preset", ["pendulum", "double_pendulum", "coupled_oscillators"])
def test_generated_notebook_runs(preset):
    system = compile_spec(preset)
    nb = build_notebook(system, duration=2.0, num_points=100)

    # Structural: valid nbformat-v4 with the expected cell mix.
    assert nb["nbformat"] == 4
    assert any(c["cell_type"] == "markdown" for c in nb["cells"])
    assert any(c["cell_type"] == "code" for c in nb["cells"])

    # Behavioural: the notebook's own code actually integrates the system.
    ns = _run_notebook_code(nb)
    assert ns["result"]["success"] is True
    assert ns["sol"]["success"] is True
    y = ns["y"]
    assert y.shape[0] == 2 * len(system.coordinates)
    assert y.shape[1] == 100


def test_notebook_embeds_the_real_dsl():
    system = compile_spec("double_pendulum")
    nb = build_notebook(system)
    code = "\n".join(code_cell_sources(nb))
    assert "\\lagrangian" in code  # provenance: the real DSL is embedded
    assert "compiler.simulate" in code


def test_cli_generate(tmp_path):
    from mechanicsdsl_notebooks.cli import main as cli_main

    rc = cli_main(["generate", "pendulum", "-o", str(tmp_path)])
    assert rc == 0
    produced = list(tmp_path.glob("*.ipynb"))
    assert produced, "no notebook generated"

    import json

    nb = json.loads(produced[0].read_text(encoding="utf-8"))
    assert nb["nbformat"] == 4
