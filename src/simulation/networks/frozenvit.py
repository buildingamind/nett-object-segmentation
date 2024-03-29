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
from networks.disembodied_models.models.vit_contrastive import VisionTransformer,LitClassifier,ViTConfigExtended,Backbone

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class FrozenViT(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: gym.spaces.Box, features_dim: int = 384):
        super(FrozenViT, self).__init__(observation_space, features_dim)
        self.n_input_channels = observation_space.shape[0]
        n_input_channels = observation_space.shape[0]
        

        #self.model = LitClassifier.load_from_checkpoint(p)
        #self.model.fc = nn.Identity()
        configuration = ViTConfigExtended()
        configuration.image_size = 64
        configuration.patch_size = 8
        configuration.num_hidden_layers = 3
        configuration.num_attention_heads = 3
        # print configuration parameters of ViT
        print('image_size - ', configuration.image_size)
        print('patch_size - ', configuration.patch_size)
        print('num_classes - ', configuration.num_classes)
        print('hidden_size - ', configuration.hidden_size)
        print('intermediate_size - ', configuration.intermediate_size)
        print('num_hidden_layers - ', configuration.num_hidden_layers)
        print('num_attention_heads - ', configuration.num_attention_heads)
        backbone = Backbone('vit', configuration)
        
        self.model = LitClassifier(backbone).backbone
        self.model.fc = nn.Identity()
        
        
    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.model(observations)