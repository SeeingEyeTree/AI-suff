import argparse
import os
import random
from collections import deque

import numpy as np
import torch
from torch import nn, optim

from agent import DQNAgent, EpsilonScheduler
from config import TrainingConfig
from replay_buffer import ReplayBuffer, Transition
from wrappers import TorchObsWrapper, make_env


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def evaluate(agent: DQNAgent, env_id: str, config: TrainingConfig) -> float:
    env = TorchObsWrapper(make_env(env_id, config.seed, render_mode=None))
    scores = []
    for _ in range(config.num_eval_episodes):
        obs, _ = env.reset(seed=config.seed)
        done = False
        episode_reward = 0.0
        while not done:
            action = agent.act(obs, epsilon=0.0)
            next_obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            episode_reward += reward
            obs = next_obs
        scores.append(episode_reward)
    env.close()
    return float(np.mean(scores))


def train(config: TrainingConfig) -> None:
    device = torch.device(config.device if torch.cuda.is_available() else "cpu")
    set_seed(config.seed)

    env = TorchObsWrapper(make_env(config.env_id, config.seed))
    num_actions = env.action_space.n

    agent = DQNAgent(num_actions, device)
    optimizer = optim.Adam(agent.online.parameters(), lr=config.learning_rate)
    replay_buffer = ReplayBuffer(config.replay_size)
    scheduler = EpsilonScheduler(config.epsilon_start, config.epsilon_end, config.epsilon_decay_frames)

    obs, _ = env.reset(seed=config.seed)
    episode_reward = 0.0
    episode_rewards = deque(maxlen=100)

    for frame_idx in range(1, config.total_frames + 1):
        epsilon = scheduler.value(frame_idx)
        action = agent.act(obs, epsilon)
        next_obs, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        replay_buffer.add(Transition(obs, action, float(reward), next_obs, done))
        obs = next_obs
        episode_reward += reward

        if done:
            episode_rewards.append(episode_reward)
            obs, _ = env.reset()
            episode_reward = 0.0

        if len(replay_buffer) >= config.min_replay_size and frame_idx % config.train_interval == 0:
            states, actions, rewards, next_states, dones = replay_buffer.sample(
                config.batch_size, device
            )
            q_values = agent.online(states).gather(1, actions.unsqueeze(1)).squeeze(1)
            with torch.no_grad():
                target_q = agent.target(next_states).max(1).values
                target = rewards + config.gamma * target_q * (1 - dones.float())
            loss = nn.functional.smooth_l1_loss(q_values, target)
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(agent.online.parameters(), 10.0)
            optimizer.step()

        if frame_idx % config.target_update_interval == 0:
            agent.update_target()

        if frame_idx % config.eval_interval == 0:
            avg_score = evaluate(agent, config.env_id, config)
            print(f"Frame {frame_idx}: avg eval score {avg_score:.2f}")

    os.makedirs(os.path.dirname(config.save_path), exist_ok=True)
    torch.save(agent.online.state_dict(), config.save_path)
    env.close()


def parse_args() -> TrainingConfig:
    parser = argparse.ArgumentParser(description="Train a DQN agent on Atari Asteroids.")
    parser.add_argument("--total-frames", type=int, default=TrainingConfig.total_frames)
    parser.add_argument("--device", type=str, default=TrainingConfig.device)
    parser.add_argument("--save-path", type=str, default=TrainingConfig.save_path)
    args = parser.parse_args()
    return TrainingConfig(
        total_frames=args.total_frames,
        device=args.device,
        save_path=args.save_path,
    )


if __name__ == "__main__":
    train(parse_args())
