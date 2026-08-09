import numpy as np
import gymnasium as gym

# Strategy:
#   - Accelerate in direction of motion: action = sign(velocity)
#   - Unless position < 0.5: use max positive acceleration (+1)
# Goal is at position >= 0.45; max position is 0.6.

N_EPISODES = 50
env = gym.make("MountainCarContinuous-v0")
episode_rewards = []
successes = 0

for ep in range(N_EPISODES):
    obs, _ = env.reset()
    total_reward = 0.0
    reached_goal = False

    while True:
        position, velocity = obs

        if position < -0.5:
            action = 1.0
        else:
            action = np.sign(velocity) if velocity != 0.0 else 1.0

        obs, reward, terminated, truncated, _ = env.step(np.array([action]))
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

print(f"\nHeuristic results over {N_EPISODES} episodes:")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
print(f"  Success rate:  {successes}/{N_EPISODES} ({100*successes/N_EPISODES:.0f}%)")
