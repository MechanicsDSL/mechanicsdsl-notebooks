<p align="center">
  <img src="https://raw.githubusercontent.com/MechanicsDSL/mechanicsdsl/main/docs/images/logo.png" alt="MechanicsDSL Logo" width="360">
</p>

<h1 align="center">mechanicsdsl-notebooks</h1>

<p align="center">
  <em>Curated Jupyter notebooks spanning all eight MechanicsDSL physics domains.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-green" alt="Active">
  <img src="https://img.shields.io/badge/notebooks-5-blue" alt="5 Notebooks">
  <a href="https://mybinder.org/v2/gh/MechanicsDSL/mechanicsdsl-notebooks/main"><img src="https://mybinder.org/badge_logo.svg" alt="Launch Binder"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/MechanicsDSL/mechanicsdsl"><img src="https://img.shields.io/badge/core-mechanicsdsl-blue" alt="Core Package"></a>
</p>

## Available Notebooks

| # | Notebook | Topics | Level |
|---|----------|--------|-------|
| 01 | [Double Pendulum](notebooks/01_double_pendulum.ipynb) | Chaos, Lyapunov exponents, phase portraits, energy conservation | Intermediate |
| 02 | [Coupled Oscillators](notebooks/02_coupled_oscillators.ipynb) | Normal modes, beating, modal decomposition, FFT verification | Intermediate |
| 03 | [Constraints](notebooks/03_constraints.ipynb) | Lagrange multipliers, Baumgarte stabilization, parameter study | Intermediate |
| 04 | [Central Forces](notebooks/04_central_forces.ipynb) | Kepler problem, orbital types, dual Noether conservation | Advanced |
| 05 | [Hamiltonian Mechanics](notebooks/05_hamiltonian.ipynb) | Phase space, separatrix, symplectic vs RK4 over 500 s | Advanced |

More notebooks in development, see [docs/index.md](docs/index.md) for the full planned curriculum.

---

## Launch

**Binder (no install required):**

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MechanicsDSL/mechanicsdsl-notebooks/main)

**Local:**

```bash
pip install mechanicsdsl-core[jupyter]
git clone https://github.com/MechanicsDSL/mechanicsdsl-notebooks
cd mechanicsdsl-notebooks
jupyter lab
```

---

## Repository Structure

```
mechanicsdsl-notebooks/
├── notebooks/              # Jupyter notebooks (numbered sequentially)
│   ├── 01_double_pendulum.ipynb
│   ├── 02_coupled_oscillators.ipynb
│   ├── 03_constraints.ipynb
│   ├── 04_central_forces.ipynb
│   └── 05_hamiltonian.ipynb
├── binder/                 # Binder environment configuration
│   ├── environment.yml
│   └── postBuild
├── docs/                   # Documentation
│   ├── index.md            # Full curriculum index
│   └── notation.md         # DSL notation reference
├── scripts/
│   ├── check_notebooks.py  # Execute and validate all notebooks
│   └── generate_index.py   # Auto-regenerate docs/index.md
└── tests/
    └── test_notebooks_run.py
```

---

## Curated vs generated notebooks

The five curated notebooks above are hand-written SciPy walkthroughs of the
physics: they show the DSL specification for each system but integrate their
own equations of motion. Notebooks *generated* by this package go through
`mechanicsdsl-core` end to end: the DSL is compiled, the equations of motion
are derived symbolically, and the system is integrated by core.

## Generate notebooks from any DSL spec

```bash
pip install mechanicsdsl-notebooks
mechanicsdsl-notebooks generate double_pendulum -o notebooks/
mechanicsdsl-notebooks generate double_pendulum --sections all --execute -o notebooks/
mechanicsdsl-notebooks generate my_system.msl --sections phase,energy,sweep --sweep k
mechanicsdsl-notebooks build-all --sections all --execute -o gallery/
mechanicsdsl-notebooks check notebooks/*.ipynb
```

| Section | Contents |
|---------|----------|
| `overview` (always) | DSL, derived equations of motion, core integration, trajectory plot |
| `phase` | phase portraits (q vs q̇) for every coordinate |
| `energy` | E = Σ q̇ ∂L/∂q̇ − L derived symbolically, energy and relative-drift plots |
| `sweep` | one parameter scaled 0.5×–1.5×, trajectories overlaid |
| `integrators` | core's RK45 / RK23 / DOP853 / LSODA against a tight reference: error and wall time |

`--execute` runs the notebook headlessly (no Jupyter needed) and stores text
and figure outputs, so the `.ipynb` renders with results on GitHub.
`check` executes existing notebooks the same way and reports any cell errors.
`build-all` writes one notebook per core preset plus a `README.md` index.

---

## For Instructors

Notebooks are designed for direct classroom use, no prior DSL knowledge assumed. Each opens with physics motivation, introduces DSL syntax progressively, and includes interactive parameter exploration. If you use these notebooks in a course, open an issue to be acknowledged in the documentation.

---

## Testing

```bash
pip install -e ".[dev]"
mechanicsdsl-notebooks check notebooks/*.ipynb   # execute all curated notebooks headlessly
pytest tests/ -v                                 # structure + every generated section executed
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Domain coverage especially needed: rigid body, perturbation theory, quantum tunneling, electromagnetism, general relativity.

## Citation

```bibtex
@software{mechanicsdsl2026,
  author = {Parsons, Noah},
  title  = {{MechanicsDSL Notebooks}},
  year   = {2026},
  doi    = {10.5281/zenodo.17771040},
  url    = {https://github.com/MechanicsDSL/mechanicsdsl-notebooks}
}
```

## License

MIT License; see [LICENSE](LICENSE).
