# Asteroids RL (Gymnasium)

This module provides a minimal DQN training framework for the Atari Asteroids environment using Gymnasium and the Arcade Learning Environment (ALE).

## Setup

Install dependencies (CPU-only example):

```bash
pip install "gymnasium[atari]" "gymnasium[accept-rom-license]" torch
```

The `accept-rom-license` extra is required for the Atari ROMs. See the Gymnasium ALE docs for details.

## Training

```bash
python -m asteroids_rl.train --total-frames 1000000 --device cuda
```

Checkpoints are saved to `checkpoints/asteroids_dqn.pt` by default.

## Evaluation

```bash
python -m asteroids_rl.eval --save-path checkpoints/asteroids_dqn.pt --episodes 5
```

## Notes

- The training loop uses Atari preprocessing (grayscale, frame skip, and frame stacking) with a DQN network similar to the original DeepMind Atari setup.
- Adjust `TrainingConfig` in `config.py` to tune hyperparameters.
