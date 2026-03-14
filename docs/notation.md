# DSL Notation Reference

This document describes the MechanicsDSL notation used throughout the notebooks.

## Keywords

| Keyword | Description | Example |
|---------|-------------|---------|
| `\system` | System name | `\system{double_pendulum}` |
| `\parameter` | Physical constant | `\parameter{m}{1.0}{kg}` |
| `\lagrangian` | Lagrangian expression | `\lagrangian{0.5*m*l^2*\dot{theta}^2 - m*g*l*(1-cos(theta))}` |
| `\hamiltonian` | Hamiltonian (alternative to Lagrangian) | `\hamiltonian{p^2/(2*m) + 0.5*m*omega^2*q^2}` |
| `\constraint` | Holonomic constraint $g=0$ | `\constraint{x^2 + y^2 - R^2}` |
| `\initial` | Initial conditions | `\initial{theta: 0.3, theta_dot: 0.0}` |
| `\target` | Code generation backend | `\target{python_numpy}` |
| `\solve` | Solver settings | `\solve{t_span: [0, 10], dt: 0.005}` |

## Coordinate Conventions

| Notation | Meaning |
|----------|---------|
| `theta` | Generalised coordinate $\theta$ |
| `\dot{theta}` | Time derivative $\dot{\theta}$ |
| `\ddot{theta}` | Second time derivative $\ddot{\theta}$ (output only) |
| `x_dot` | Alternative dot notation |

## Supported Targets

| Target string | Output |
|---------------|--------|
| `python_numpy` | NumPy function for `scipy.integrate.solve_ivp` |
| `python_jax` | JAX-jitted function with autodiff |
| `cpp` | Standalone C++ with Eigen |
| `cuda` | CUDA kernel |
| `rust` | Rust with `ndarray` |
| `julia` | Julia with `DifferentialEquations.jl` |
| `fortran` | Modern Fortran 90+ |
| `arduino` | Arduino `.ino` with fixed-point option |
| `ros2` | ROS2 C++ node package |
| `unity` | Unity C# `MonoBehaviour` |
| `unreal` | Unreal Engine C++ `UActorComponent` |
| `webassembly` | WASM via Emscripten |

## Mathematical Operations

Standard mathematical operations are supported in LaTeX-inspired notation:

```
sin(x), cos(x), tan(x), asin(x), acos(x), atan2(y,x)
sqrt(x), exp(x), log(x), abs(x)
x^2, x^n
\frac{a}{b}  or  a/b
```
