#!/usr/bin/env python3

from networks.resnet10 import  CustomResnet10CNN
from networks.resnet18 import CustomResnet18CNN
from networks.frozenvit import FrozenViT


from networks.ego4d import Ego4D

from networks.dino import  DinoV2, DinoV1
from networks.frozensimclr import FrozenSimCLR
from networks.ego4d import Ego4D
from networks.segmentanything import SegmentAnything

 

# encoder_config.py
ENCODERS = {
        "small": {
            "feature_dimensions": 512,  # replace with actual feature dimensions for 'small'
            "encoder": "",
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
        "encoder": DinoV1,
    },
    "simclr": {
        "feature_dimensions": 512,  # replace with actual feature dimensions for 'ego4d'
        "encoder": FrozenSimCLR,
    }, 
    "sam": {
        "feature_dimensions": 256,  # replace with actual feature dimensions for 'sam'
        "encoder": SegmentAnything,
    },
    "ego4d":{
         "feature_dimensions": 384,  # replace with actual feature dimensions for 'ego4d'
        "encoder": Ego4D,
    }
}