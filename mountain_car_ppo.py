import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# MountainCarContinuous-v0
# State:  [position (-1.2 to 0.6), velocity (-0.07 to 0.07)]
# Action: [force (-1 to 1)]
# Reward: +100 on reaching goal, -0.1 * action^2 per step (sparse + costly)

print("Training PPO on MountainCarContinuous-v0...")
vec_env = make_vec_env("MountainCarContinuous-v0", n_envs=4)
model = PPO("MlpPolicy", vec_env, verbose=1, n_steps=2048, batch_size=64, n_epochs=10)
model.learn(total_timesteps=300_000)
vec_env.close()
model.save("mountain_car_ppo")
print("Training done. Model saved to mountain_car_ppo.zip\n")

# Evaluate
N_EPISODES = 50
env = gym.make("MountainCarContinuous-v0")
episode_rewards = []
successes = 0

for ep in range(N_EPISODES):
    obs, _ = env.reset()
    total_reward = 0.0
    reached_goal = False

    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, _ = env.step(action)
        total_reward += reward
        if obs[0] >= 0.45:
            reached_goal = True
        if terminated or truncated:
            break

    episode_rewards.append(total_reward)
    if reached_goal:
        successes += 1
    if (ep + 1) % 10 == 0:
        print(f"Episode {ep+1}/{N_EPISODES}  avg so far: {np.mean(episode_rewards):.2f}")

env.close()

print(f"\nPPO results over {N_EPISODES} episodes:")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
print(f"  Success rate:  {successes}/{N_EPISODES} ({100*successes/N_EPISODES:.0f}%)")
