import numpy as np
import gymnasium as gym
from gymnasium import spaces
from scipy import linalg
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env


class HybridPendulumEnv(gym.Wrapper):
    """Pendulum-v1 with a 2D action space: [torque, lqr_gate].
    If lqr_gate > 0, the LQR controller decides the torque.
    Otherwise, torque * 2.0 is applied (rescaling [-1,1] to [-2,2]).
    """

    def __init__(self, render_mode=None):
        super().__init__(gym.make("Pendulum-v1", render_mode=render_mode))
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

        # LQR setup (identical to pendulum_render.py)
        g, m, l = 10.0, 1.0, 1.0
        A = np.array([[0, 1], [3*g/(2*l), 0]])
        B = np.array([[0], [3/(m*l**2)]])
        Q = np.array([[1.0, 0.0], [0.0, 0.1]])
        R = np.array([[0.001]])
        P = linalg.solve_continuous_are(A, B, Q, R)
        self.K = np.linalg.inv(R) @ B.T @ P

    def _lqr_torque(self, obs):
        cos_theta, sin_theta, theta_dot = obs
        theta = np.arctan2(sin_theta, cos_theta)
        return float(np.clip((-self.K @ [theta, theta_dot])[0], -2.0, 2.0))

    def step(self, action):
        if action[1] > 0:
            torque = self._lqr_torque(self._last_obs)
        else:
            torque = float(np.clip(action[0] * 2.0, -2.0, 2.0))

        obs, reward, terminated, truncated, info = self.env.step([torque])
        self._last_obs = obs
        return obs, reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._last_obs = obs
        return obs, info


# Train
print("Training Hybrid PPO (ent_coef=0.05)...")
vec_env = make_vec_env(HybridPendulumEnv, n_envs=4)
model = PPO("MlpPolicy", vec_env, ent_coef=0.05, verbose=1)
model.learn(total_timesteps=200_000)
vec_env.close()
model.save("pendulum_ppo_hybrid")
print("Training done. Model saved to pendulum_ppo_hybrid.zip\n")

# Evaluate
N_EPISODES = 200
env = HybridPendulumEnv()
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

print(f"\nHybrid PPO+LQR results over {N_EPISODES} episodes:")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
print()
print("Baselines for comparison:")
print("  PPO only:      mean -419, std ±151")
print("  LQR + swing:   mean -694, std ±489")

# Render
print("\nRendering — close the window or Ctrl+C to stop.")
render_env = HybridPendulumEnv(render_mode="human")
obs, _ = render_env.reset()
try:
    while True:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, terminated, truncated, _ = render_env.step(action)
        if terminated or truncated:
            obs, _ = render_env.reset()
finally:
    render_env.close()
