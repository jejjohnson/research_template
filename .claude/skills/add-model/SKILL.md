---
name: add-model
description: Add a model to the research project — a class in the package's models subpackage whose constructor arguments are its config keys, a Hydra config-group option (configs/model/<name>.yaml), the hydra-zen config, the training script wiring that builds it from the config, tests, and the capability index. Use when asked to add, port or implement a model, baseline, architecture or estimator in src/myproject/models and configs/model.
---

# Add a model

<!-- template-example: example-specific paths (src/myproject/models, configs/model, scripts/train.py, scripts/train_zen.py); keep the procedure, rewrite the names after adoption. -->

Read "Boundaries" and contracts 1 and 2 in `AGENTS.md` first; this is the
step-by-step.

## 1. Make sure it does not exist yet

- `docs/api/capabilities.md` (`myproject.models.*`): a model that differs
  only in sizes is a new config option for the existing class, not a new
  class.
- `configs/model/`: the option may exist already. (`transformer.yaml`
  exists as a config only: no class reads it yet, and it lacks the
  `hidden_size` key `scripts/train.py` reads.)
- A model from a library (scikit-learn, PyTorch, …) needs a thin wrapper
  only if it must match the project's interface; otherwise configure the
  library class directly.

## 2. The class (`src/myproject/models/<name>.py`)

Follow `BaselineModel` (`models/baseline.py`):

- keyword constructor arguments with defaults, stored under their own
  names — they are exactly the keys of its config file;
- the computation in methods (`forward(x)` in the example; whatever the
  trainer calls), with no file IO, config reading or global RNG; weights
  initialised from a seed or generator passed in, or after
  `seed_everything` by the entry point;
- a `__repr__` showing the configuration;
- type hints and a Google-style docstring with the model's equation
  (Unicode) and its reference (add the entry to `references.bib`);
- a new framework dependency (torch, jax, …) goes into `pixi.toml` (then
  `pixi lock`); `seed_everything` already seeds PyTorch when it is
  installed.

## 3. The config (`configs/model/<name>.yaml`)

```yaml
name: <name>
hidden_size: 64
num_layers: 2
```

- Every constructor argument, with the same default as the class, plus
  `name`. Every key the training script reads from `cfg.model` must be
  there, or `model=<name>` fails with a missing-key error.
- Choose it with `model=<name>`, or make it the default in the `defaults`
  list of `configs/train.yaml`.

## 4. Wire it into training

`scripts/train.py` builds `BaselineModel` from `cfg.model.hidden_size` and
`cfg.model.num_layers`. With a second model, let the config choose the
class: give each model file a `_target_` and build it with
`hydra.utils.instantiate`, dropping the `name` key the constructor does not
take:

```python
from hydra.utils import instantiate
from omegaconf import OmegaConf

model_cfg = OmegaConf.masked_copy(cfg.model, [k for k in cfg.model if k != "name"])
# configs/model/<name>.yaml holds `_target_: myproject.models.<module>.<Class>`
model = instantiate(model_cfg)
```

In `scripts/train_zen.py`, add `builds(NewModel, populate_full_signature=True)`
and register it with `store(..., name="<name>", group="model")`, so the
hydra-zen config is generated from the same signature.

## 5. Tests (`tests/test_models.py`)

Follow the `BaselineModel` tests: defaults, custom parameters, `repr`, and
the forward pass on a tiny input against a hand computation (shape, a
known value, determinism for a fixed seed). Training-loop behaviour goes
in a trainer test with a few epochs on toy data, well under a second.

## 6. Pipeline, export and docs

- The `train` stage depends on `src/myproject/models` and `configs/`
  already; a model in a new package directory joins its `deps`.
- `make capabilities`, and commit `docs/api/capabilities.md`.
- Describe the architecture in `docs/notes/methods.md` (the
  `write-up-results` skill).

## 7. Verify

```bash
uv run pytest tests/test_models.py -v -o addopts=
make capabilities && uv run pytest tests/test_capabilities.py -o addopts=
pixi run train model=<name> training.epochs=2
```

Then the `pre-pr-check` skill.
