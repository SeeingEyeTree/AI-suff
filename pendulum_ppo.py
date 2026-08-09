import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Train
print("Training PPO...")
vec_env = make_vec_env("Pendulum-v1", n_envs=4)
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=200_000)
vec_env.close()
model.save("pendulum_ppo")
print("Training done. Model saved to pendulum_ppo.zip\n")

# Evaluate
N_EPISODES = 200
env = gym.make("Pendulum-v1")
episode_rewards = []

for ep in range(N_EPISODES):
    obs, _ = env.reset()
    total_reward = 0.0

    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        total_reward += reward
        if terminated or truncated:
            break

    episode_rewards.append(total_reward)
    if (ep + 1) % 50 == 0:
        print(f"Episode {ep+1}/{N_EPISODES}  avg so far: {np.mean(episode_rewards):.2f}")

env.close()

print(f"\nPPO results over {N_EPISODES} episodes:")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
