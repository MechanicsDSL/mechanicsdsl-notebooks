<p align="center">
  <img src="https://raw.githubusercontent.com/MechanicsDSL/mechanicsdsl/main/docs/images/logo.png" alt="MechanicsDSL Logo" width="360">
</p>

<h1 align="center">mechanicsdsl-notebooks</h1>

<p align="center">
  <em>Curated Jupyter notebooks spanning all eight MechanicsDSL physics domains.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-planned-lightgrey" alt="Status: Planned">
  <a href="https://mybinder.org/v2/gh/MechanicsDSL/mechanicsdsl-notebooks/main"><img src="https://mybinder.org/badge_logo.svg" alt="Launch Binder"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/MechanicsDSL/mechanicsdsl"><img src="https://img.shields.io/badge/core-mechanicsdsl-blue" alt="Core Package"></a>
</p>

---

## Overview

`mechanicsdsl-notebooks` is the official curriculum and demonstration notebook collection for MechanicsDSL. Each notebook pairs DSL source with physics exposition, derivation context, interactive widgets, and annotated simulation output — from introductory pendulum problems through graduate-level general relativistic geodesics.

Notebooks are designed to be launchable in Binder with zero local setup, and structured to serve as standalone course material for instructors adopting MechanicsDSL.

---

## Planned Notebook Collection

### Classical Mechanics

| Notebook | Topics | Level |
|----------|--------|-------|
| `01_simple_pendulum.ipynb` | DSL basics, Lagrangian derivation, phase portrait | Introductory |
| `02_double_pendulum.ipynb` | Chaos, Lyapunov exponents, sensitivity to initial conditions | Intermediate |
| `03_coupled_oscillators.ipynb` | Normal modes, eigenanalysis, beating phenomena | Intermediate |
| `04_constraints.ipynb` | Lagrange multipliers, Baumgarte stabilization, bead on wire | Intermediate |
| `05_rigid_body.ipynb` | Euler angles, quaternions, symmetric top, Euler's equations | Advanced |
| `06_central_forces.ipynb` | Effective potential, Kepler problem, orbital precession | Advanced |
| `07_canonical_transformations.ipynb` | Generating functions, action-angle variables, Hamilton-Jacobi | Advanced |
| `08_perturbation_theory.ipynb` | Lindstedt-Poincaré, averaging method, driven oscillators | Advanced |
| `09_noether_theorem.ipynb` | Symmetry detection, cyclic coordinates, conservation law monitoring | Intermediate |
| `10_sph_fluid.ipynb` | Smoothed Particle Hydrodynamics, dam break, surface tension | Expert |

### Other Physics Domains

| Notebook | Domain | Level |
|----------|--------|-------|
| `11_quantum_tunneling.ipynb` | Quantum Mechanics | Intermediate |
| `12_hydrogen_atom.ipynb` | Quantum Mechanics | Intermediate |
| `13_lorentz_force.ipynb` | Electromagnetism | Introductory |
| `14_schwarzschild_geodesics.ipynb` | General Relativity | Advanced |
| `15_kerr_orbits.ipynb` | General Relativity — Rotating black holes | Expert |
| `16_ising_model.ipynb` | Statistical Mechanics | Intermediate |
| `17_carnot_cycle.ipynb` | Thermodynamics | Introductory |
| `18_three_body.ipynb` | Classical Mechanics — Figure-8 orbit | Advanced |

### Applied & Integration Notebooks

| Notebook | Topics | Level |
|----------|--------|-------|
| `19_parameter_estimation.ipynb` | Inverse problems, adjoint gradients, fitting to data | Advanced |
| `20_mcmc_uncertainty.ipynb` | Hamiltonian Monte Carlo, posterior distributions | Expert |
| `21_sobol_sensitivity.ipynb` | Global sensitivity analysis, parameter importance | Advanced |
| `22_jax_ensemble.ipynb` | `jax.vmap` phase space exploration, GPU batching | Advanced |
| `23_ros2_export.ipynb` | Generating ROS2 packages from notebook workflows | Expert |
| `24_embedded_export.ipynb` | Generating Arduino and Raspberry Pi code from notebooks | Advanced |

---

## Usage

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

## For Instructors

Notebooks are structured for direct classroom use:

- Each notebook opens with a concise physics motivation requiring no prior DSL knowledge
- DSL syntax is introduced progressively — no programming assumed in early notebooks
- Interactive `ipywidgets` sliders allow parameter exploration without editing code
- Export cells at the end of each notebook demonstrate generating C++, Julia, or other backend code from the same specification

If you are using these notebooks in a course, we encourage you to open an issue linking your course — we are happy to acknowledge courses using MechanicsDSL in the documentation.

---

## Status

This repository is in the planning stage. Initial notebooks will draw from the 30+ example scripts already included in the core package. Watch this repository or the [core repo](https://github.com/MechanicsDSL/mechanicsdsl) for updates.

---

## Contributing

Notebook contributions are particularly welcome — especially worked examples from novel physics domains or real course deployments. See [CONTRIBUTING.md](https://github.com/MechanicsDSL/mechanicsdsl/blob/main/CONTRIBUTING.md).

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <a href="https://github.com/MechanicsDSL/mechanicsdsl">Core Package</a> ·
  <a href="https://mechanicsdsl.readthedocs.io">Documentation</a> ·
  <a href="https://doi.org/10.5281/zenodo.17771040">Zenodo DOI</a>
</p>
