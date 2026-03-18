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

## Who's Using MechanicsDSL?

We can see from our download analytics that MechanicsDSL is being used across **54+ countries** and mirrored by institutions worldwide — but PyPI doesn't tell us who you are.

If you're using MechanicsDSL in research, education, industry, or a personal project, we'd love to hear from you. It takes 60 seconds and helps guide the project's direction.

**[→ Tell us about your use case](https://tally.so/r/XxqOqP)**

*All responses are voluntary and confidential. We will not contact you without permission.*

---

## Available Notebooks

| # | Notebook | Topics | Level |
|---|----------|--------|-------|
| 01 | [Double Pendulum](notebooks/01_double_pendulum.ipynb) | Chaos, Lyapunov exponents, phase portraits, energy conservation | Intermediate |
| 02 | [Coupled Oscillators](notebooks/02_coupled_oscillators.ipynb) | Normal modes, beating, modal decomposition, FFT verification | Intermediate |
| 03 | [Constraints](notebooks/03_constraints.ipynb) | Lagrange multipliers, Baumgarte stabilization, parameter study | Intermediate |
| 04 | [Central Forces](notebooks/04_central_forces.ipynb) | Kepler problem, orbital types, dual Noether conservation | Advanced |
| 05 | [Hamiltonian Mechanics](notebooks/05_hamiltonian.ipynb) | Phase space, separatrix, symplectic vs RK4 over 500 s | Advanced |

More notebooks in development — see [docs/index.md](docs/index.md) for the full planned curriculum.

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

## What MechanicsDSL Does in Each Notebook

Every notebook includes the DSL specification that the MechanicsDSL compiler uses to automatically:
- Derive equations of motion via the Euler-Lagrange equations symbolically
- Identify conserved quantities via Noether's theorem
- Generate NumPy, JAX, or other backend simulation code

Example from Notebook 05:
```
\system{pendulum_hamiltonian}
\parameter{m}{1.0}{kg}
\parameter{l}{1.0}{m}
\lagrangian{0.5*m*l^2*\dot{theta}^2 - m*g*l*(1-cos(theta))}
\target{python_numpy}
```
MechanicsDSL derives: $H = p_\theta^2/(2ml^2) + mgl(1-\cos\theta)$ and generates Hamilton's equations automatically.

---

## For Instructors

Notebooks are designed for direct classroom use — no prior DSL knowledge assumed. Each opens with physics motivation, introduces DSL syntax progressively, and includes interactive parameter exploration. If you use these notebooks in a course, open an issue to be acknowledged in the documentation.

---

## Testing

```bash
pip install pytest nbconvert
python scripts/check_notebooks.py       # execute all notebooks
pytest tests/ -v                        # validate structure
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

MIT License — see [LICENSE](LICENSE).
