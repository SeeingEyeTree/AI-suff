import gymnasium as gym
import numpy as np
import torch
from gymnasium.wrappers import AtariPreprocessing, FrameStack


def make_env(env_id: str, seed: int, render_mode: str | None = None) -> gym.Env:
    env = gym.make(env_id, render_mode=render_mode)
    env = AtariPreprocessing(env, scale_obs=True, grayscale_obs=True, frame_skip=4)
    env = FrameStack(env, num_stack=4)
    env.action_space.seed(seed)
    env.observation_space.seed(seed)
    return env


class TorchObsWrapper(gym.ObservationWrapper):
    def __init__(self, env: gym.Env):
        super().__init__(env)
        obs_shape = self.observation_space.shape
        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(obs_shape[-1], obs_shape[0], obs_shape[1]),
            dtype=np.float32,
        )

    def observation(self, observation: np.ndarray) -> torch.Tensor:
        obs = np.array(observation, copy=False)
        obs = np.transpose(obs, (2, 0, 1))
        return torch.tensor(obs, dtype=torch.float32)
