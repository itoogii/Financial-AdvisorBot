

import torch.nn as nn

class QNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Conv1d(5, out_channels=64, kernel_size=5),
            nn.ReLU(),
            nn.Conv1d(64, out_channels=128, kernel_size=3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(128 * 54, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 3),
        )

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(0) 
        x = x.transpose(1, 2) # Changing the shape from (1, 60, 5) to (1, 5, 60)
        return self.network(x)
