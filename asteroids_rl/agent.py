from dataclasses import dataclass

import torch
from torch import nn


class DQN(nn.Module):
    def __init__(self, num_actions: int) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(4, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
        )
        self.head = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 7 * 7, 512),
            nn.ReLU(),
            nn.Linear(512, num_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        return self.head(x)


@dataclass
class EpsilonScheduler:
    start: float
    end: float
    decay_frames: int

    def value(self, frame_idx: int) -> float:
        fraction = min(frame_idx / self.decay_frames, 1.0)
        return self.start + fraction * (self.end - self.start)


class DQNAgent:
    def __init__(self, num_actions: int, device: torch.device) -> None:
        self.device = device
        self.online = DQN(num_actions).to(device)
        self.target = DQN(num_actions).to(device)
        self.target.load_state_dict(self.online.state_dict())
        self.target.eval()

    def act(self, state: torch.Tensor, epsilon: float) -> int:
        if torch.rand(1).item() < epsilon:
            return torch.randint(0, self.online.head[-1].out_features, (1,)).item()
        with torch.no_grad():
            q_values = self.online(state.unsqueeze(0).to(self.device))
        return int(torch.argmax(q_values, dim=1).item())

    def update_target(self) -> None:
        self.target.load_state_dict(self.online.state_dict())
