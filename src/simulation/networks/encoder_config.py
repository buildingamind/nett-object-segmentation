#!/usr/bin/env python3

from networks import  CustomResnet10CNN, CustomResnet18CNN, DinoV2, FrozenSimCLR, SegmentAnything
from stable_baselines3.common.models import NatureCNN
 

# encoder_config.py
ENCODERS = {
        "small": {
            "feature_dimensions": 512,  # replace with actual feature dimensions for 'small'
            "encoder": NatureCNN,
        },
    "medium": {
        "feature_dimensions": 128,  # replace with actual feature dimensions for 'medium'
        "encoder": CustomResnet10CNN,
    },
    "large": {
        "feature_dimensions": 128,  # replace with actual feature dimensions for 'large'
        "encoder": CustomResnet18CNN,
    },
    "dinov2": {
        "feature_dimensions": 384,  # replace with actual feature dimensions for 'dinov2'
        "encoder": DinoV2,
    },
    "dinov1": {
        "feature_dimensions": 384,  # replace with actual feature dimensions for 'dinov1',
        "encoder": DinoV2,
    },
    "simclr": {
        "feature_dimensions": 512,  # replace with actual feature dimensions for 'ego4d'
        "encoder": FrozenSimCLR,
    }, 
    "sam": {
        "feature_dimensions": 384,  # replace with actual feature dimensions for 'sam'
        "encoder": SegmentAnything,
    }
}