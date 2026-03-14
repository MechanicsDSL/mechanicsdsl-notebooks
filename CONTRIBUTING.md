# Contributing to mechanicsdsl-notebooks

## Adding a Notebook

Good notebook contributions follow this structure:

1. **Title cell** — `# System Name: Key Concept 1, Key Concept 2`
2. **Metadata line** — `**MechanicsDSL Notebook NN** | Domain | Level`
3. **Physics background** — derivation from first principles with DSL specification
4. **Code cells** — imports, parameters, EOM, simulations, plots
5. **Summary table** — key results in a markdown table
6. **Next notebook link** — `**Next:** [NN+1 — Title](filename.ipynb)`

## Naming Convention

`NN_descriptive_name.ipynb` where `NN` is the two-digit sequence number.

## Quality Standards

- All notebooks must execute without errors in Binder
- Each notebook must include the MechanicsDSL DSL specification for the system
- Conservation laws identified by MechanicsDSL must be verified numerically
- Figures must have axis labels and titles

## Testing Your Notebook

```bash
pip install mechanicsdsl-core jupyter nbconvert
jupyter nbconvert --to notebook --execute your_notebook.ipynb
python scripts/check_notebooks.py --notebook notebooks/your_notebook.ipynb
```

## Updating the Index

After adding a notebook, regenerate the index:

```bash
python scripts/generate_index.py
```

## Domain Coverage Needed

Currently missing notebooks (contributions especially welcome):

| # | Topic | Domain | Difficulty |
|---|-------|--------|-----------|
| 06 | Rigid Body / Symmetric Top | Classical | Advanced |
| 07 | Perturbation Theory | Classical | Advanced |
| 08 | Quantum Tunneling (WKB) | Quantum | Intermediate |
| 09 | Lorentz Force / Cyclotron | EM | Introductory |
| 10 | Schwarzschild Geodesics | GR | Expert |
