from dataclasses import dataclass


@dataclass
class TrainingConfig:
    env_id: str = "ALE/Asteroids-v5"
    seed: int = 42
    total_frames: int = 1_000_000
    learning_rate: float = 1e-4
    gamma: float = 0.99
    batch_size: int = 32
    replay_size: int = 100_000
    min_replay_size: int = 10_000
    target_update_interval: int = 10_000
    train_interval: int = 4
    eval_interval: int = 50_000
    epsilon_start: float = 1.0
    epsilon_end: float = 0.01
    epsilon_decay_frames: int = 500_000
    max_episode_steps: int | None = None
    num_eval_episodes: int = 5
    device: str = "cuda"
    save_path: str = "checkpoints/asteroids_dqn.pt"
