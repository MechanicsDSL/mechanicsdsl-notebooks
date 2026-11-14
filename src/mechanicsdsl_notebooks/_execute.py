"""
_execute.py
-----------
Execute a notebook *without Jupyter* and store its outputs.

Code cells run in order in one shared namespace (exactly as a kernel would).
Printed text becomes ``stream`` outputs, every matplotlib figure a cell
creates becomes an ``image/png`` ``display_data`` output, and an exception
becomes an ``error`` output. The result is a normal executed ``.ipynb`` that
renders with outputs on GitHub, nbviewer and in JupyterLab.

This is what lets ``mechanicsdsl-notebooks generate --execute`` and
``build-all --execute`` ship notebooks with results already in them, and lets
CI prove that every generated notebook actually runs.
"""

from __future__ import annotations

import base64
import contextlib
import copy
import io
import time
import traceback
from typing import Dict, List, Tuple


class NotebookExecutionError(RuntimeError):
    """Raised by :func:`execute_notebook` when a cell fails and ``allow_errors`` is False."""


def _stream(text: str) -> Dict:
    return {"output_type": "stream", "name": "stdout", "text": text.splitlines(keepends=True)}


def _figure_outputs(plt, already: set, dpi: int) -> List[Dict]:
    outs = []
    for num in plt.get_fignums():
        if num in already:
            continue
        fig = plt.figure(num)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
        outs.append({
            "output_type": "display_data",
            "data": {
                "image/png": base64.b64encode(buf.getvalue()).decode("ascii"),
                "text/plain": [f"<Figure {num}>"],
            },
            "metadata": {},
        })
        plt.close(fig)
    return outs


def execute_notebook(notebook: Dict, *, allow_errors: bool = False, dpi: int = 80,
                     timeout_per_cell: float = 600.0) -> Tuple[Dict, Dict]:
    """Run every code cell; return ``(executed_notebook, namespace)``.

    The input notebook is not modified. ``timeout_per_cell`` is reported, not
    enforced (Python cannot safely interrupt in-process code); a cell that
    exceeds it is noted in the cell metadata.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    nb = copy.deepcopy(notebook)
    ns: Dict = {"__name__": "__main__"}
    plt.close("all")
    real_show = plt.show
    plt.show = lambda *a, **k: None  # figures are captured after each cell instead
    try:
        return _run_cells(nb, ns, plt, allow_errors, dpi, timeout_per_cell)
    finally:
        plt.show = real_show


def _run_cells(nb, ns, plt, allow_errors, dpi, timeout_per_cell):
    count = 0
    for idx, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        count += 1
        src = "".join(cell["source"])
        out = io.StringIO()
        outputs: List[Dict] = []
        start = time.perf_counter()
        failed = None
        with contextlib.redirect_stdout(out):
            try:
                exec(compile(src, f"<cell {count}>", "exec"), ns)  # noqa: S102
            except Exception as exc:  # recorded as a notebook error output
                failed = exc
        elapsed = time.perf_counter() - start
        if out.getvalue():
            outputs.append(_stream(out.getvalue()))
        outputs += _figure_outputs(plt, set(), dpi)
        if failed is not None:
            outputs.append({
                "output_type": "error",
                "ename": type(failed).__name__,
                "evalue": str(failed),
                "traceback": traceback.format_exception_only(type(failed), failed),
            })
        cell["outputs"] = outputs
        cell["execution_count"] = count
        cell["metadata"]["mechanicsdsl_elapsed_s"] = round(elapsed, 4)
        if elapsed > timeout_per_cell:
            cell["metadata"]["mechanicsdsl_slow"] = True
        if failed is not None and not allow_errors:
            raise NotebookExecutionError(
                f"cell {count} (notebook cell {idx}) raised "
                f"{type(failed).__name__}: {failed}"
            ) from failed
    return nb, ns
