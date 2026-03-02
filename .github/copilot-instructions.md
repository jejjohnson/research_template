# Copilot Instructions

This is a scientific research project template. Follow these conventions:

## Environment

- Use `pixi run <task>` for all commands (never `pip install` or `conda install` directly)
- Python >= 3.12, type annotations required
- Use `from __future__ import annotations` for forward references

## Code Style

- Ruff linting + formatting (line-length 88)
- Select: E, F, I, UP, B, SIM, RUF

## Project Conventions

- Data files managed by DVC (never commit raw data to git)
- Configs managed by Hydra in `configs/` directory
- Results saved to `results/` (DVC-managed)
- Notebooks stripped of outputs (nbstripout pre-commit hook)

## Testing

```bash
pixi run test        # Run tests
pixi run lint        # Lint
pixi run typecheck   # Type check
```
