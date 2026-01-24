from collections import deque
from dataclasses import dataclass
from typing import Deque, Tuple

import numpy as np
import torch


@dataclass
class Transition:
    state: torch.Tensor
    action: int
    reward: float
    next_state: torch.Tensor
    done: bool


class ReplayBuffer:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.buffer: Deque[Transition] = deque(maxlen=capacity)

    def add(self, transition: Transition) -> None:
        self.buffer.append(transition)

    def __len__(self) -> int:
        return len(self.buffer)

    def sample(self, batch_size: int, device: torch.device) -> Tuple[torch.Tensor, ...]:
        indices = np.random.choice(len(self.buffer), size=batch_size, replace=False)
        states = torch.stack([self.buffer[i].state for i in indices]).to(device)
        actions = torch.tensor([self.buffer[i].action for i in indices], device=device)
        rewards = torch.tensor([self.buffer[i].reward for i in indices], device=device)
        next_states = torch.stack([self.buffer[i].next_state for i in indices]).to(device)
        dones = torch.tensor([self.buffer[i].done for i in indices], device=device)
        return states, actions, rewards, next_states, dones
