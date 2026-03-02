# Coding Agent Instructions

This document provides instructions for AI coding agents working on this
research project.

## Environment Setup

This project uses [Pixi](https://pixi.sh) for environment management.
All commands should be run using `pixi run <task>`.

```bash
# Install all environments
pixi install

# Install specific environment
pixi install -e jupyterlab
```

## Project Structure

```
research_template/
├── configs/          # Hydra configuration hierarchy
├── data/             # Data directories (managed by DVC)
├── docs/             # MyST documentation
├── marimo_notebooks/ # Marimo reactive notebooks
├── notebooks/        # Jupytext percent-format .py scripts (no .ipynb in repo)
├── results/          # Experiment results (managed by DVC)
├── scripts/          # Entry point scripts
├── src/myproject/    # Source package
└── tests/            # Test suite
```

## Development Commands

```bash
# Run tests
pixi run test

# Lint code
pixi run lint

# Format code
pixi run format

# Type check
pixi run typecheck

# Run all pre-commit hooks
pixi run precommit
```

## Running Experiments

```bash
# Preprocess data
pixi run preprocess

# Train with default config
pixi run train

# Train with hydra-zen
pixi run train-zen

# Train with overrides
pixi run train training.lr=0.001 model=transformer

# Evaluate
pixi run evaluate
```

## DVC Conventions

- **Never commit raw data** to git. Use `dvc add` and `dvc push`.
- Run `dvc repro` to reproduce the full pipeline.
- Check pipeline status with `dvc status`.
- View pipeline DAG with `dvc dag`.
- Commit `.dvc` pointer files and `dvc.lock` to git.

```bash
# Add a data file to DVC tracking
dvc add data/raw/dataset.csv

# Push data to remote storage
dvc push

# Pull data from remote storage
dvc pull

# Reproduce the pipeline
dvc repro

# Check what has changed
dvc status
```

## Hydra / hydra-zen Conventions

- Config files live in `configs/`.
- Use `configs/train.yaml` as the main entry point config.
- Override values on the command line: `python scripts/train.py training.lr=0.01`.
- Use multirun for sweeps: `python scripts/train.py -m training.lr=0.001,0.01,0.1`.
- hydra-zen configs are defined in `scripts/train_zen.py` using `builds()` and `make_config()`.

## Documentation

```bash
# Serve docs locally
pixi run -e docs docs-serve

# Build static HTML
pixi run -e docs docs-build
```

## Notebook Environments

```bash
# JupyterLab
pixi run -e jupyterlab lab

# Marimo
pixi run -e marimo marimo-edit
```

## Code Style

- Python >= 3.12
- Ruff for linting and formatting (line-length 88)
- Type annotations required for all public functions
- Use `from __future__ import annotations` for forward references
