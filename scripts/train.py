"""Training entry point using Hydra for configuration management."""

from __future__ import annotations

import hydra
from omegaconf import DictConfig

from myproject.models.baseline import BaselineModel
from myproject.trainers.trainer import Trainer
from myproject.utils.reproducibility import seed_everything


@hydra.main(version_base=None, config_path="../configs", config_name="train")
def main(cfg: DictConfig) -> None:
    """Main training function.

    Args:
        cfg: Hydra configuration object. Automatically populated from
             configs/train.yaml and any overrides passed on the command line.

    Example usage:
        # Use defaults from configs/train.yaml
        python scripts/train.py

        # Override specific parameters
        python scripts/train.py training.lr=0.001 model=transformer

        # Multirun sweep
        python scripts/train.py -m training.lr=0.001,0.01,0.1
    """
    # Set random seed for reproducibility
    seed_everything(cfg.training.seed)

    # Initialize model from config
    model = BaselineModel(
        hidden_size=cfg.model.hidden_size,
        num_layers=cfg.model.num_layers,
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        lr=cfg.training.lr,
        epochs=cfg.training.epochs,
    )

    # Run training (data loading omitted for placeholder)
    metrics = trainer.train(train_data=None)

    print(f"Training complete. Final metrics: {metrics}")


if __name__ == "__main__":
    main()
