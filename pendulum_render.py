import gymnasium as gym
import numpy as np
from scipy import linalg

# Pendulum-v1 parameters
g = 10.0
m = 1.0
l = 1.0

# Linearized dynamics around upright (theta=0, unstable equilibrium)
# theta_ddot = (3g/2l)*theta + (3/ml^2)*torque
A = np.array([[0,          1],
              [3*g/(2*l),  0]])   # [[0,1],[15,0]]

B = np.array([[0],
              [3/(m*l**2)]])      # [[0],[3]]

# Cost matrices matching the reward: -(theta^2 + 0.1*theta_dt^2 + 0.001*torque^2)
Q = np.array([[1.0, 0.0],
              [0.0, 0.1]])

R = np.array([[0.001]])

# Solve continuous-time algebraic Riccati equation -> optimal gain K
P = linalg.solve_continuous_are(A, B, Q, R)
K = np.linalg.inv(R) @ B.T @ P
print(f"LQR gain K: {K}")

N_EPISODES = 200
env = gym.make("Pendulum-v1")
episode_rewards = []

for ep in range(N_EPISODES):
    obs, _ = env.reset()
    total_reward = 0.0

    while True:
        cos_theta, sin_theta, theta_dot = obs
        theta = np.arctan2(sin_theta, cos_theta)

        if abs(theta) > 0.4:
            torque = 0.45 * np.sign(theta_dot)
        else:
            torque = float(np.clip((-K @ [theta, theta_dot])[0], -2.0, 2.0))

        obs, reward, terminated, truncated, _ = env.step([torque])
        total_reward += reward

        if terminated or truncated:
            break

    episode_rewards.append(total_reward)
    if (ep + 1) % 50 == 0:
        print(f"Episode {ep+1}/{N_EPISODES}  avg so far: {np.mean(episode_rewards):.2f}")

env.close()

print(f"\nResults over {N_EPISODES} episodes:")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
