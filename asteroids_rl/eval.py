import argparse

import torch

from asteroids_rl.agent import DQNAgent
from asteroids_rl.config import TrainingConfig
from asteroids_rl.train import evaluate
from asteroids_rl.wrappers import TorchObsWrapper, make_env


def load_agent(config: TrainingConfig) -> DQNAgent:
    env = TorchObsWrapper(make_env(config.env_id, config.seed))
    agent = DQNAgent(env.action_space.n, torch.device(config.device))
    agent.online.load_state_dict(torch.load(config.save_path, map_location=agent.device))
    agent.update_target()
    env.close()
    return agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a trained Asteroids DQN agent.")
    parser.add_argument("--save-path", type=str, default=TrainingConfig.save_path)
    parser.add_argument("--episodes", type=int, default=TrainingConfig.num_eval_episodes)
    args = parser.parse_args()

    config = TrainingConfig(save_path=args.save_path, num_eval_episodes=args.episodes)
    agent = load_agent(config)
    avg_score = evaluate(agent, config.env_id, config)
    print(f"Average score over {config.num_eval_episodes} episodes: {avg_score:.2f}")


if __name__ == "__main__":
    main()
