#!/usr/bin/env python3
import gym
import numpy as np 
from stitching import AffineStitcher
import cv2
import pdb

class ObservationWrapper(gym.ObservationWrapper):
    """
    Gym env wrapper that transpose visual observations to (C,H,W).
    """
    def __init__(self, env):
        super().__init__(env)

        # Assumes visual observation space with shape (H, W, C)
        assert isinstance(env.observation_space, gym.spaces.Box)
        assert len(env.observation_space.shape) == 3

        #h, w, c = env.observation_space.shape
        #self.observation_space = gym.spaces.Box(0, 1, dtype=np.float32, shape=(c, h, w))
        
        width, height, channels = env.observation_space.shape
        new_shape = (channels, width, height)
        self.observation_space = gym.spaces.Box(low=0.0, high=255, shape=new_shape, dtype=np.uint8)

    def observation(self, observation):
        return np.swapaxes(observation, 2, 0)
    
class StitchVisualObservationsWrapper(gym.ObservationWrapper):
    """
    Gym env wrapper that stitches visual observations from two cameras.
    """
    def __init__(self, env):
        super().__init__(env)
        self.env = env
        self.num_frames = len(self.env.observation_space)
        #old_space = env.observation_space
        
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(3,64,64), dtype=np.uint8)
        self.stitcher = AffineStitcher(detector="sift", confidence_threshold=0.0)
       

    def observation(self, observation):
        # stitch and return
        return self.stitch(observation[0], observation[1])

    # implement all stitching logic here and call it from observation()
    def stitch(self, right_eye, left_eye):
        # try to stitch
        try:
            stitched = self.stitcher.stitch([self.swap_channels(right_eye), self.swap_channels(left_eye)])
            stitched = cv2.resize(stitched, (64, 64), interpolation=cv2.INTER_AREA)
        # fall back to the first camera in case the stitching fails (doesn't happen often)
        except:
            stitched = right_eye
        
        return self.swap_channels(stitched, True)

    # helper to swap channels (cv2 requires channel first)
    def swap_channels(self, image, channels_first=False):
        if channels_first:
            return np.moveaxis(image, 2, 0)
        else:
            return np.moveaxis(image, 0, 2)
        
    def reset(self, **kwargs):
        """
        Resets the environment and returns the initial observation.

        Args:
            **kwargs: Additional keyword arguments for resetting the environment.

        Returns:
            numpy.ndarray: The initial observation.

        """
        
        obs1, obs2 = self.env.reset(**kwargs)
        
        p = self.observation([obs1,obs2])
        return p