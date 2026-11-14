"""
test_sections_and_execute.py
----------------------------
Every analysis section runs for real (headless executor, no Jupyter), outputs
are captured into the notebook, and the state-vector indexing matches core's
interleaved layout.
"""
import json

import numpy as np
import pytest

pytest.importorskip("mechanics_dsl", reason="mechanicsdsl-core required")

from mechanicsdsl_notebooks import (  # noqa: E402
    SECTIONS,
    NotebookExecutionError,
    build_notebook,
    compile_spec,
    execute_notebook,
)
from mechanicsdsl_notebooks.cli import main as cli_main  # noqa: E402


@pytest.mark.parametrize("preset", ["pendulum", "double_pendulum", "damped_oscillator",
                                    "figure8"])
def test_all_sections_execute(preset):
    system = compile_spec(preset)
    nb = build_notebook(system, duration=1.0, num_points=200, sections=SECTIONS)
    executed, ns = execute_notebook(nb)
    outputs = [o for c in executed["cells"] for o in c.get("outputs", [])]
    assert not [o for o in outputs if o["output_type"] == "error"]
    assert any("image/png" in o.get("data", {}) for o in outputs), "no figure captured"
    assert all(c["execution_count"] for c in executed["cells"] if c["cell_type"] == "code")
    if system.conservative:
        assert ns["drift"].max() < 1e-4  # core's default tolerances
    # the input notebook is left untouched
    assert all(c.get("outputs") == [] for c in nb["cells"] if c["cell_type"] == "code")


def test_coordinates_are_indexed_by_name_not_position():
    # core returns y interleaved as [theta1, theta1_dot, theta2, theta2_dot].
    nb = build_notebook(compile_spec("double_pendulum"), duration=1.0, num_points=50)
    _, ns = execute_notebook(nb)
    sv = list(ns["sol"]["state_vars"])
    assert np.array_equal(ns["Q"][1], ns["y"][sv.index("theta2")])
    assert np.array_equal(ns["QD"][0], ns["y"][sv.index("theta1_dot")])


def test_sweep_uses_requested_parameter():
    nb = build_notebook(compile_spec("pendulum"), duration=1.0, num_points=50,
                        sections=["sweep"], sweep_parameter="l")
    _, ns = execute_notebook(nb)
    assert ns["SWEEP_PARAM"] == "l"


def test_unknown_section_rejected():
    with pytest.raises(ValueError):
        build_notebook(compile_spec("pendulum"), sections=["bogus"])


def test_execution_error_is_reported():
    nb = build_notebook(compile_spec("pendulum"), duration=1.0, num_points=20)
    nb["cells"].append({"cell_type": "code", "metadata": {}, "execution_count": None,
                        "outputs": [], "source": ["raise ValueError('boom')"]})
    with pytest.raises(NotebookExecutionError):
        execute_notebook(nb)
    executed, _ = execute_notebook(nb, allow_errors=True)
    assert executed["cells"][-1]["outputs"][-1]["ename"] == "ValueError"


def test_cli_generate_execute_and_check(tmp_path):
    assert cli_main(["generate", "pendulum", "--sections", "phase,energy", "--execute",
                     "--duration", "1", "--points", "50", "-o", str(tmp_path)]) == 0
    path = tmp_path / "simple_pendulum.ipynb"
    nb = json.loads(path.read_text(encoding="utf-8"))
    assert nb["metadata"]["mechanicsdsl"]["sections"] == ["overview", "phase", "energy"]
    assert any(c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code")
    assert cli_main(["check", str(path)]) == 0


def test_cli_build_all(tmp_path):
    assert cli_main(["build-all", "--duration", "0.5", "--points", "20",
                     "-o", str(tmp_path)]) == 0
    index = (tmp_path / "README.md").read_text(encoding="utf-8")
    notebooks = list(tmp_path.glob("*.ipynb"))
    assert len(notebooks) >= 8
    assert all(nb.name in index for nb in notebooks)


def test_cli_rejects_bad_section():
    with pytest.raises(SystemExit):
        cli_main(["generate", "pendulum", "--sections", "nope"])
