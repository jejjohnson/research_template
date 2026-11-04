---
applyTo: "src/**/*.py,tests/**/*.py,scripts/**/*.py"
---

# Python Coding Standards

The house style is the maintainer's `python-style` skill; `AGENTS.md` ("House style") carries its essentials. This file is the short form for Copilot.

## Modern Python (3.12+)

- `from __future__ import annotations` at the top of every module
- Type hints on **all** public functions, methods, and module-level variables
- Modern union syntax: `X | None` not `Optional[X]`, `X | Y` not `Union[X, Y]`
- Built-in generics: `list[int]`, `dict[str, Any]` not `List[int]`, `Dict[str, Any]`
- `pathlib.Path` over `os.path`
- f-strings for string formatting
- `dataclasses` or `attrs` for data containers
- `Enum` for fixed sets of constants
- Context managers (`with` statements) for resource handling
- Specific exception types (never bare `except:`)
- Proper exception chaining (`raise ... from ...`)
- Early returns / guard clauses to reduce nesting

## Where code goes

- Reusable logic lives in the package under `src/`, takes plain arguments (never a Hydra `DictConfig`) and has a test; `scripts/` read the config, call the package and write outputs (see "Boundaries" in `/AGENTS.md`).
- Every setting a run depends on is a key in `configs/`, not a literal.
- Seed once per run from the config; pass a `numpy.random.Generator` down rather than drawing from global state.

## Package Preferences

A runtime dependency goes into `pixi.toml` (and `pixi.lock` is regenerated); never `pip install` / `conda install` by hand.

| Purpose | Preferred Package |
|---------|-------------------|
| Configuration | `hydra-core` / `omegaconf`, `hydra-zen` |
| Data and pipeline versioning | `dvc` |
| Labelled arrays, NetCDF | `xarray`, `netcdf4` |
| Data containers | `dataclasses` (stdlib) or `attrs` |
| Logging and script output | `loguru` (never stdlib `logging` or progress `print`s) |
| CLI arguments (non-Hydra scripts) | `cyclopts` (never argparse, click or typer) |
| Path handling | `pathlib` (stdlib) |
| HTTP | `httpx` |
| Testing | `pytest` |

## Comments and naming

- Comments go above the line, never beside it; they say *why*, not *what*
- A Unicode equation above each mathematical line (`# ŷ = W x + b`), in the `eman-style-math` notation
- Descriptive names (`posterior_precision`, not `Lam`); the symbol lives only in the equation comment
- One operation per line; step headers (`# --- whiten ---`) split a long function into stages
- In JAX code: jaxtyping with named dims, einx (no `axis=`, `.T`, `reshape`, `[:, None]`), lineax for solves, `eqx.Module` with `__check_init__` and `eqx.error_if`

## Documentation

- Module-level docstrings explaining purpose
- Function/method docstrings for all public APIs (Google style)
- Docstrings open with a one-line summary and the defining equation in Unicode (`σ² = ∑ᵢ (xᵢ − μ)² / N`), never `$…$`; a function that implements a method adds a numbered `Algorithm:` section; `Args:` give each name's meaning and symbol, without the type
- Public classes and functions include a short usage example where it helps a reader
