import numpy as np
import torch
import gymnasium as gym
from replaybuffer import ReplayBuffer

# Gymnasium Spaces for observations and actions
observation_space = gym.spaces.Box(
    low=-np.inf, high=np.inf, shape=(60, 5), dtype=np.float32
)
action_space = gym.spaces.Discrete(3, dtype=np.int32)

# ReplayBuffer object with size=10
test_rb = ReplayBuffer(10, observation_space, action_space, optimize_memory_usage=True)

# Create a test observation
test_obs = np.ones((1, 60, 5), dtype=np.float32)

# Add experiences
test_rb.add(test_obs, test_obs, 1, 1.0, False)
test_rb.add(test_obs, test_obs, 0, 2.0, True)
test_rb.add(test_obs, test_obs, 0, 1.0, False)
test_rb.add(test_obs, test_obs, 1, 0.0, True)
test_rb.add(test_obs, test_obs, 1, 1.0, True)


def test_replay_buffer_size():
    assert test_rb.size() == 5


def test_replay_buffer_shapes():
    # Sample 3 experiences
    sample = test_rb.sample(3)
    # Check shapes
    assert sample.observations.shape[0] == 3
    assert sample.next_observations.shape[0] == 3
    assert sample.actions.shape[0] == 3
    assert sample.rewards.shape[0] == 3
    assert sample.dones.shape[0] == 3


def test_replay_buffer_dtypes():
    # Sample 3 experiences
    sample = test_rb.sample(3)

    # Check that rewards are floats
    assert sample.rewards.dtype == torch.float32

    # Check that actions are int8
    assert sample.actions.dtype == torch.int32
    # Check that actions are in [0, 1]
    assert np.all(np.isin(sample.actions.cpu().numpy(), [0, 1]))

    # Check that dones are integers (0 or 1)
    assert sample.dones.dtype == torch.int8
    assert np.all(np.isin(sample.dones.cpu().numpy(), [0, 1]))
