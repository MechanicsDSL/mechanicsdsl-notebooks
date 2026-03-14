# MechanicsDSL Notebooks

## Notebook Index

| # | Notebook | Domain | Level | Key Concepts |
|---|----------|--------|-------|--------------|
| 01 | [Double Pendulum](notebooks/01_double_pendulum.ipynb) | Classical Mechanics | Intermediate | Chaos, Lyapunov exponents, phase portraits |
| 02 | [Coupled Oscillators](notebooks/02_coupled_oscillators.ipynb) | Classical Mechanics | Intermediate | Normal modes, beating, modal decomposition |
| 03 | [Constraints](notebooks/03_constraints.ipynb) | Classical Mechanics | Intermediate | Lagrange multipliers, Baumgarte stabilization |
| 04 | [Central Forces](notebooks/04_central_forces.ipynb) | Classical Mechanics | Advanced | Kepler problem, orbital mechanics, Noether |
| 05 | [Hamiltonian Mechanics](notebooks/05_hamiltonian.ipynb) | Classical Mechanics | Advanced | Phase space, symplectic structure |
| 06 | [Rigid Body](notebooks/06_rigid_body.ipynb) | Classical Mechanics | Advanced | Euler angles, symmetric top, precession |
| 07 | [Perturbation Theory](notebooks/07_perturbation_theory.ipynb) | Classical Mechanics | Advanced | Lindstedt-Poincaré, secular terms |
| 08 | [Quantum Tunneling](notebooks/08_quantum_tunneling.ipynb) | Quantum Mechanics | Intermediate | WKB, transmission coefficient |
| 09 | [Special Relativity](notebooks/09_special_relativity.ipynb) | Special Relativity | Intermediate | Lorentz kinematics, four-vectors |
| 10 | [Statistical Mechanics](notebooks/10_statistical_mechanics.ipynb) | Statistical Mechanics | Intermediate | Partition functions, Boltzmann distribution |

## Launch in Binder

[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MechanicsDSL/mechanicsdsl-notebooks/main)

## Local Installation

```bash
pip install mechanicsdsl-core[jupyter]
git clone https://github.com/MechanicsDSL/mechanicsdsl-notebooks
cd mechanicsdsl-notebooks
jupyter lab
```

## MechanicsDSL DSL Quick Reference

Every notebook includes the DSL specification that MechanicsDSL uses to derive equations of motion:

```
\system{name}
\parameter{symbol}{value}{unit}
\lagrangian{expression}
\constraint{expression}   % optional
\initial{coord: value}
\target{python_numpy}     % or python_jax, cpp, rust, julia, ...
\solve{t_span: [0, T], dt: 0.005}
```
