import numpy as np
import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.callbacks import BaseCallback
from collections import deque
from rich.live import Live
from rich.table import Table
from rich.text import Text

TOTAL_STEPS = 100_000
HEIGHT_SCALE = 0.3   # weak shaping weight — increase if agent still doesn't learn


class HeightRewardWrapper(gym.Wrapper):
    """Adds scale * sin(3 * position) to reward — gives dense signal for climbing."""
    def __init__(self, env, scale=HEIGHT_SCALE):
        super().__init__(env)
        self.scale = scale

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        position = obs[0]
        return obs, reward + self.scale * np.sin(3 * position), terminated, truncated, info


class LiveStatsCallback(BaseCallback):
    def __init__(self, total_timesteps, update_freq=500, verbose=0):
        super().__init__(verbose)
        self.total_timesteps = total_timesteps
        self.update_freq = update_freq
        self.ep_rewards = deque(maxlen=20)
        self.ep_lengths = deque(maxlen=20)
        self.successes = 0
        self.n_episodes = 0
        self.best_reward = -np.inf
        self._live = None

    def _make_table(self):
        pct = 100 * self.num_timesteps / self.total_timesteps
        avg_r = np.mean(self.ep_rewards) if self.ep_rewards else float("nan")
        avg_l = np.mean(self.ep_lengths) if self.ep_lengths else float("nan")
        success_rate = 100 * self.successes / max(1, self.n_episodes)
        ent = self.model.ent_coef_tensor.item() if hasattr(self.model, "ent_coef_tensor") else "?"

        bar_filled = int(pct / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)

        t = Table(
            title=f"[bold cyan]MountainCar SAC[/bold cyan]  {bar}  [white]{pct:.1f}%[/white]",
            show_header=True,
            header_style="bold",
            min_width=42,
        )
        t.add_column("Stat", style="dim")
        t.add_column("Value", justify="right", style="bold white")

        t.add_row("Steps", f"{self.num_timesteps:,} / {self.total_timesteps:,}")
        t.add_row("Avg Reward (last 20)", f"{avg_r:.2f}")
        t.add_row("Best Reward (shaped)", f"{self.best_reward:.2f}")
        t.add_row("Avg Episode Length", f"{avg_l:.0f}")
        t.add_row("Episodes", str(self.n_episodes))
        t.add_row("Success Rate", f"{success_rate:.0f}%")
        t.add_row("Entropy Coef", f"{ent:.5f}" if isinstance(ent, float) else str(ent))
        return t

    def _on_training_start(self):
        self._live = Live(self._make_table(), refresh_per_second=4, transient=False)
        self._live.start()

    def _on_step(self):
        for info in self.locals.get("infos", []):
            if "episode" in info:
                r = info["episode"]["r"]
                l = info["episode"]["l"]
                self.ep_rewards.append(r)
                self.ep_lengths.append(l)
                self.n_episodes += 1
                if r > 90:
                    self.successes += 1
                if r > self.best_reward:
                    self.best_reward = r

        if self.num_timesteps % self.update_freq == 0 and self._live:
            self._live.update(self._make_table())

        return True

    def _on_training_end(self):
        if self._live:
            self._live.update(self._make_table())
            self._live.stop()


print("Training SAC on MountainCarContinuous-v0 (height shaping)...")
env = HeightRewardWrapper(gym.make("MountainCarContinuous-v0"))
callback = LiveStatsCallback(total_timesteps=TOTAL_STEPS)
model = SAC("MlpPolicy", env, verbose=0, learning_starts=1000, ent_coef="auto")
model.learn(total_timesteps=TOTAL_STEPS, callback=callback)
env.close()
model.save("mountain_car_sac")
print("Model saved to mountain_car_sac.zip\n")

# Evaluate on raw env (no shaping) to get true performance
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
print(f"\nSAC results over {N_EPISODES} episodes (raw env, no shaping):")
print(f"  Mean reward:   {np.mean(episode_rewards):.2f}")
print(f"  Std:           {np.std(episode_rewards):.2f}")
print(f"  Min:           {np.min(episode_rewards):.2f}")
print(f"  Max:           {np.max(episode_rewards):.2f}")
print(f"  Success rate:  {successes}/{N_EPISODES} ({100*successes/N_EPISODES:.0f}%)")
