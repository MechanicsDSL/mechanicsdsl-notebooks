"""
_generate.py
------------
Generate runnable Jupyter notebooks from MechanicsDSL specifications.

A notebook is just an ``nbformat`` v4 JSON document, so this module builds one
directly without importing ``nbformat``; generation has no Jupyter
dependency. Every notebook compiles the DSL spec through ``mechanicsdsl-core``
and then adds the requested analysis *sections*:

``overview``     equations of motion, core integration, trajectory plot (always on)
``phase``        phase portraits (q vs q_dot) for every coordinate
``energy``       energy E = sum(qdot dL/dqdot) - L derived symbolically, drift plot
``sweep``        a parameter sweep: one parameter varied over 0.5x..1.5x
``integrators``  core's RK45 / DOP853 / LSODA compared on accuracy and runtime

The code cells are ordinary Python and run with or without a Jupyter kernel
(see :func:`code_cell_sources` and :mod:`._execute`).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterable, List, Optional

if TYPE_CHECKING:
    from ._bridge import CompiledSystem

SECTIONS = ("overview", "phase", "energy", "sweep", "integrators")
DEFAULT_SECTIONS = ("overview",)


def _md(text: str) -> Dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def _code(text: str) -> Dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def code_cell_sources(notebook: Dict) -> List[str]:
    """Return the concatenated source of each code cell (for headless testing)."""
    return [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    ]


def _overview(system: "CompiledSystem", duration: float, num_points: int) -> List[Dict]:
    return [
        _code("from mechanics_dsl import PhysicsCompiler\n"
              "import numpy as np\n"
              "import sympy as sp\n"
              "import matplotlib.pyplot as plt"),
        _md("## 1. DSL specification\n\n"
            "The system below is compiled by `mechanicsdsl-core`; the "
            "equations of motion are derived symbolically from the Lagrangian."),
        _code(f'dsl = r"""\n{system.source}\n"""\n'
              "compiler = PhysicsCompiler()\n"
              "result = compiler.compile_dsl(dsl)\n"
              "assert result['success'], result.get('error')\n"
              "coordinates = compiler.get_coordinates()\n"
              "print('Compiled:', compiler.system_name)\n"
              "print('Coordinates:', coordinates)"),
        _md("## 2. Equations of motion\n\n"
            "Symbolically derived generalized accelerations."),
        _code("for name, expr in compiler.equations.items():\n"
              "    print(f'{name} = {expr}')"),
        _md(f"## 3. Simulation\n\n"
            f"Integrate for {duration:g} s ({num_points} samples) with core's "
            f"automatically selected solver."),
        _code(f"DURATION = {duration!r}\n"
              f"NUM_POINTS = {num_points}\n"
              "sol = compiler.simulate(t_span=(0.0, DURATION), num_points=NUM_POINTS)\n"
              "assert sol['success'], sol.get('message')\n"
              "t = sol['t']\n"
              "y = sol['y']\n"
              "n_dof = len(coordinates)\n"
              "# core's state vector is interleaved [q1, q1_dot, q2, q2_dot, ...];\n"
              "# index it by name rather than by position.\n"
              "state_vars = list(sol['state_vars'])\n"
              "Q = np.array([y[state_vars.index(c)] for c in coordinates])\n"
              "QD = np.array([y[state_vars.index(c + '_dot')] for c in coordinates])\n"
              "print('Integrated', len(t), 'steps;', sol['method_used'])"),
        _md("## 4. Trajectory\n\nGeneralized coordinates versus time."),
        _code("fig, ax = plt.subplots(figsize=(9, 4))\n"
              "for i, c in enumerate(coordinates):\n"
              "    ax.plot(t, Q[i], label=c)\n"
              "ax.set_xlabel('t [s]')\n"
              "ax.set_ylabel('generalized coordinate')\n"
              f"ax.set_title('{system.name}')\n"
              "ax.legend()\n"
              "ax.grid(True, alpha=0.3)\n"
              "fig.tight_layout()"),
    ]


def _phase(system: "CompiledSystem") -> List[Dict]:
    return [
        _md("## Phase portraits\n\n"
            "Each coordinate against its own velocity. Closed curves indicate "
            "periodic motion; filling a region suggests quasi-periodic or chaotic motion."),
        _code("ncols = min(n_dof, 3)\n"
              "nrows = -(-n_dof // ncols)\n"
              "fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3.5 * nrows),\n"
              "                         squeeze=False)\n"
              "for i, c in enumerate(coordinates):\n"
              "    ax = axes[i // ncols][i % ncols]\n"
              "    ax.plot(Q[i], QD[i], lw=0.8)\n"
              "    ax.plot(Q[i][0], QD[i][0], 'o', label='start')\n"
              "    ax.set_xlabel(c)\n"
              "    ax.set_ylabel(c + '_dot')\n"
              "    ax.grid(True, alpha=0.3)\n"
              "for j in range(n_dof, nrows * ncols):\n"
              "    axes[j // ncols][j % ncols].axis('off')\n"
              "fig.tight_layout()"),
    ]


def _energy(system: "CompiledSystem") -> List[Dict]:
    note = ("" if system.conservative else
            "\n\n**This system declares non-conservative forces or damping, so "
            "energy is expected to change.**")
    return [
        _md("## Energy\n\n"
            "The Jacobi energy $E = \\sum_i \\dot q_i\\,\\partial L/\\partial \\dot q_i - L$ "
            "is derived symbolically from the compiled Lagrangian and evaluated "
            "along the trajectory. For a conservative system its relative drift "
            "measures the integrator's error." + note),
        _code("L = compiler.symbolic.ast_to_sympy(compiler.lagrangian)\n"
              "by_name = {str(s): s for s in L.free_symbols}\n"
              "E_expr = -L\n"
              "for c in coordinates:\n"
              "    v = by_name.get(c + '_dot')\n"
              "    if v is not None:\n"
              "        E_expr += v * sp.diff(L, v)\n"
              "E_expr = sp.simplify(E_expr)\n"
              "print('E =', E_expr)\n"
              "param_values = {k: float(v['value']) for k, v in compiler.parameters_def.items()}\n"
              "state_syms = [by_name.get(n, sp.Symbol(n)) for n in\n"
              "              list(coordinates) + [c + '_dot' for c in coordinates]]\n"
              "E_fn = sp.lambdify(state_syms, E_expr.subs(\n"
              "    {by_name[k]: v for k, v in param_values.items() if k in by_name}), 'numpy')\n"
              "E = np.asarray(E_fn(*Q, *QD), dtype=float) * np.ones_like(t)\n"
              "drift = np.abs(E - E[0]) / max(abs(E[0]), 1e-12)\n"
              "print(f'max relative energy drift: {drift.max():.3e}')"),
        _code("fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.5))\n"
              "a1.plot(t, E)\n"
              "a1.set_xlabel('t [s]'); a1.set_ylabel('E'); a1.set_title('Energy')\n"
              "a2.semilogy(t[1:], np.maximum(drift[1:], 1e-17))\n"
              "a2.set_xlabel('t [s]'); a2.set_ylabel('|E-E0|/|E0|')\n"
              "a2.set_title('Relative drift')\n"
              "for a in (a1, a2): a.grid(True, alpha=0.3)\n"
              "fig.tight_layout()"),
    ]


_RHS_HELPER = (
    "from scipy.integrate import solve_ivp\n"
    "\n"
    "def make_rhs(param_values):\n"
    "    \"\"\"First-order RHS from compiler.equations with explicit parameters.\"\"\"\n"
    "    eqs = compiler.equations\n"
    "    syms = {}\n"
    "    exprs = list(eqs['__mass_matrix__']) if '__mass_matrix__' in eqs else list(eqs.values())\n"
    "    for e in exprs:\n"
    "        syms.update({str(s): s for s in e.free_symbols})\n"
    "    state = [syms.get(n, sp.Symbol(n)) for n in\n"
    "             list(coordinates) + [c + '_dot' for c in coordinates]]\n"
    "    subs = {syms[k]: v for k, v in param_values.items() if k in syms}\n"
    "    if '__mass_matrix__' in eqs:\n"
    "        M, F = eqs['__mass_matrix__']\n"
    "        Mf = sp.lambdify(state, M.subs(subs), 'numpy')\n"
    "        Ff = sp.lambdify(state, F.subs(subs), 'numpy')\n"
    "        acc = lambda *s: np.linalg.solve(np.asarray(Mf(*s), float),\n"
    "                                         np.asarray(Ff(*s), float).ravel())\n"
    "    else:\n"
    "        fns = [sp.lambdify(state, eqs[c + '_ddot'].subs(subs), 'numpy')\n"
    "               for c in coordinates]\n"
    "        acc = lambda *s: np.array([float(f(*s)) for f in fns])\n"
    "    def rhs(_t, s):\n"
    "        return np.concatenate([s[n_dof:], acc(*s)])\n"
    "    return rhs\n"
    "\n"
    "base_params = {k: float(v['value']) for k, v in compiler.parameters_def.items()}\n"
    "y0 = np.concatenate([Q[:, 0], QD[:, 0]])  # make_rhs uses [q..., q_dot...]\n"
)


def _sweep(system: "CompiledSystem", parameter: Optional[str]) -> List[Dict]:
    params = sorted(system.parameters)
    if not params:
        return []
    if parameter is None:
        # Prefer a parameter the dynamics actually depend on.
        used = set().union(*[{str(s) for s in e.free_symbols}
                             for e in system.equations.values()])
        parameter = next((p for p in params if p in used), params[0])
    return [
        _md(f"## Parameter sweep: `{parameter}`\n\n"
            f"`{parameter}` is scaled from 0.5x to 1.5x of its DSL value and the "
            f"first coordinate is re-integrated (DOP853, rtol 1e-9). Change "
            f"`SWEEP_PARAM` to sweep a different parameter: {', '.join(params)}."),
        _code(_RHS_HELPER),
        _code(f"SWEEP_PARAM = {parameter!r}\n"
              "factors = [0.5, 0.75, 1.0, 1.25, 1.5]\n"
              "fig, ax = plt.subplots(figsize=(9, 4))\n"
              "for f in factors:\n"
              "    pv = dict(base_params)\n"
              "    pv[SWEEP_PARAM] = base_params[SWEEP_PARAM] * f\n"
              "    s = solve_ivp(make_rhs(pv), (t[0], t[-1]), y0, t_eval=t,\n"
              "                  method='DOP853', rtol=1e-9, atol=1e-11)\n"
              "    ax.plot(s.t, s.y[0], label=f'{SWEEP_PARAM} = {pv[SWEEP_PARAM]:.4g}')\n"
              "ax.set_xlabel('t [s]'); ax.set_ylabel(coordinates[0])\n"
              "ax.legend(fontsize=8); ax.grid(True, alpha=0.3)\n"
              "fig.tight_layout()"),
    ]


def _integrators(system: "CompiledSystem") -> List[Dict]:
    return [
        _md("## Integrator comparison\n\n"
            "Core's solvers against a tight DOP853 reference (rtol 1e-12): final-state "
            "error and wall time."),
        _code("import time\n"
              "ref = compiler.simulate(t_span=(0.0, DURATION), num_points=NUM_POINTS,\n"
              "                        method='DOP853', rtol=1e-12, atol=1e-14)\n"
              "rows = []\n"
              "for method in ['RK45', 'RK23', 'DOP853', 'LSODA']:\n"
              "    t0 = time.perf_counter()\n"
              "    s = compiler.simulate(t_span=(0.0, DURATION), num_points=NUM_POINTS,\n"
              "                          method=method, rtol=1e-6, atol=1e-9)\n"
              "    dt_wall = time.perf_counter() - t0\n"
              "    err = float(np.max(np.abs(s['y'][:, -1] - ref['y'][:, -1])))\n"
              "    rows.append((method, err, dt_wall))\n"
              "print(f\"{'method':<8} {'final-state error':>18} {'wall [s]':>10}\")\n"
              "for m, e, w in rows:\n"
              "    print(f'{m:<8} {e:>18.3e} {w:>10.4f}')"),
    ]


def build_notebook(system: "CompiledSystem", *, duration: float = 10.0,
                   num_points: int = 1000,
                   sections: Iterable[str] = DEFAULT_SECTIONS,
                   sweep_parameter: Optional[str] = None) -> Dict:
    """Build an nbformat-v4 notebook dict for ``system``.

    ``sections`` is any subset of :data:`SECTIONS`; ``overview`` is always
    included because every other section uses its results.
    """
    sections = list(dict.fromkeys(["overview", *sections]))
    unknown = [s for s in sections if s not in SECTIONS]
    if unknown:
        raise ValueError(f"unknown section(s) {unknown}; choose from {SECTIONS}")

    coords = ", ".join(system.coordinates)
    cells = [
        _md(f"# {system.name}\n\n"
            f"Auto-generated by **mechanicsdsl-notebooks** from a MechanicsDSL "
            f"specification. This notebook compiles the DSL, derives the "
            f"equations of motion, integrates the dynamics, and plots the "
            f"trajectory.\n\n"
            f"Generalized coordinates: `{coords}`  \n"
            f"Sections: {', '.join(sections)}"),
    ]
    cells += _overview(system, duration, num_points)
    if "phase" in sections:
        cells += _phase(system)
    if "energy" in sections and system.energy is not None:
        cells += _energy(system)
    if "sweep" in sections:
        cells += _sweep(system, sweep_parameter)
    if "integrators" in sections:
        cells += _integrators(system)

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python"},
            "mechanicsdsl": {"generated": True, "system": system.name,
                             "sections": sections},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
