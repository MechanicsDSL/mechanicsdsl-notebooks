# Changelog

All notable changes to mechanicsdsl-notebooks are documented here.

## [0.2.0] - 2026-11-14

### Added
- Composable notebook sections: `phase`, `energy`, `sweep` and `integrators`, on top of `overview` (`--sections all`).
- Headless execution without Jupyter (`--execute`, `execute_notebook()`): stdout, figures and errors are stored as real notebook outputs.
- `build-all` (one notebook per core preset, plus an index), `check` (execute existing notebooks and report errors) and `presets` commands.
- Shared bridge to core: energy E = sum(qdot dL/dqdot) - L derived from the Lagrangian, a `conservative` flag, `simulate()` (fixed-step RK4 reference), `energy_drift()`, `operation_count()`, `list_presets()`, and `CompiledSystem.describe()`.
- Core's mass-matrix output (`__mass_matrix__`, used for large systems such as the three-body `figure8` preset) is converted to explicit accelerations, so every core preset now generates.

### Fixed
- Generated notebooks read core's solution positionally, but core interleaves the state as `[q1, q1_dot, q2, q2_dot]`, so multi-DOF trajectory plots showed `theta1_dot` labelled as `theta2`. Rows are now looked up through `sol['state_vars']`.
- `get_notebook_path()` looked for a local clone one directory above the repository.

### Documentation
- README states that the curated notebooks are hand-written SciPy walkthroughs; generated notebooks run through core.

### Infrastructure
- CI workflow: pytest on Python 3.9-3.12 (Linux) plus Windows and macOS, a syntax/undefined-name lint, and an sdist/wheel build check.
- Dependabot (pip and GitHub Actions), issue and PR templates, pre-commit config, `SECURITY.md`, `CODE_OF_CONDUCT.md`.
- Single-source version (`_version.py`, read by hatch); requires `mechanicsdsl-core>=2.1.4`.

## [Unreleased]

### Added
- `01_double_pendulum.ipynb` — chaos, phase portraits, Lyapunov exponent estimation
- `02_coupled_oscillators.ipynb` — normal modes, beating, modal decomposition, FFT verification
- `03_constraints.ipynb` — Lagrange multipliers, Baumgarte stabilization, parameter study
- `04_central_forces.ipynb` — Kepler problem, orbital types, dual Noether conservation
- Binder environment configuration (`binder/environment.yml`, `binder/postBuild`)
- Notebook validation scripts (`scripts/check_notebooks.py`, `scripts/generate_index.py`)
- Documentation (`docs/index.md`, `docs/notation.md`)
- CI workflow for automated notebook execution on push

## [0.1.0] — 2026-03-13

- Initial repository scaffold
