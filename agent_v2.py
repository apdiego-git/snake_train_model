import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque


class Layers(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(8, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 4)

    def forward(self, x):
        x = self.layer1(x)
        x = torch.relu(x)
        x = self.layer2(x)
        x = torch.relu(x)
        x = self.layer3(x)
        return x
    
class ReplayBuffer():
    def __init__(self, capacity):
        self.agent_mem = deque(maxlen=capacity)

    def storage(self, experience):
        self.agent_mem.append(experience)
    
    def sample(self, batch_size):
        return random.sample(self.agent_mem, k=batch_size)
    
class Agent_V2():
    def __init__(self):
        self.layers = Layers()
        self.buffer = ReplayBuffer(3500)
        self.learning_rate = .25
        self.discount_factor = .90
        self.batch_size = 64
        try:
            self.exploration_rate = np.load("exploration_rate_v2.npy")
        except:
            self.exploration_rate = 1.0
        self.decay_rate = .999
        self.min_exploration = .005
        self.optimizer = optim.Adam(self.layers.parameters(), self.learning_rate)
        self.criterion = nn.MSELoss()

    def store(self, experience):
        self.buffer.storage(experience)

    def decide(self, state):
        tensor = torch.from_numpy(state)
        random_choice = random.randint(0, 3)
        if(random.random() < self.exploration_rate):
            return random_choice
        else:
            return torch.argmax(self.layers(tensor)).item()
