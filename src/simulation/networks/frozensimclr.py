#!/usr/bin/env python3
import pdb
import gym

import os
import torch as th
import torch.nn as nn
import torchvision
import timm
from torchvision.transforms import Compose
from torchvision.transforms import Resize, CenterCrop, Normalize, InterpolationMode
from networks.disembodied_models.models.simclr import SimCLR

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

checkpoint_path = os.path.join(os.getcwd(), "data/checkpoints")
    
class FrozenSimCLR(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 384, object_background="ship_A"):
        super(FrozenSimCLR, self).__init__(observation_space, features_dim)
        self.n_input_channels = observation_space.shape[0]
        n_input_channels = observation_space.shape[0]
        background = object_background.lower()
        checkpoint_file = {
            "ship_a": "simclr/ship_A/checkpoints/epoch=97-step=14601.ckpt",
            "ship_b": "simclr/ship_B/checkpoints/epoch=97-step=14601.ckpt",
            "ship_c": "simclr/ship_C/checkpoints/epoch=96-step=14452.ckpt",
            "fork_b": "simclr/fork_B/checkpoints/epoch=95-step=14303.ckpt",
            "ship_b": "simclr/ship_B/checkpoints/epoch=97-step=14601.ckpt",
            "fork_a": "simclr/fork_A/checkpoints/epoch=97-step=14601.ckpt",
            "fork_c": "simclr/fork_C/checkpoints/epoch=97-step=14601.ckpt"
        }
        
        checkpoint_file_path = os.path.join(checkpoint_path, checkpoint_file.get(background, ""))
        self.model = SimCLR.load_from_checkpoint(checkpoint_file_path)
        
        
    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.model(observations)