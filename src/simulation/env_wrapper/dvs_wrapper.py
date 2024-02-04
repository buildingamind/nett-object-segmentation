#!/usr/bin/env python3

import collections
import gym
from scipy.ndimage import gaussian_filter
import numpy as np
import matplotlib.pyplot as plt
import pdb
from PIL import Image
import os
import cv2
import pdb

class DVSWrapper(gym.ObservationWrapper):
    """
    A gym observation wrapper that performs Dynamic Vision Sensor (DVS) transformation on the environment observations.

    Args:
        env (gym.Env): The environment to wrap.
        change_threshold (int): The threshold value for detecting changes in pixel intensity.
        kernel_size (tuple): The size of the Gaussian kernel used for blurring.
        sigma (float): The standard deviation of the Gaussian kernel.

    Attributes:
        change_threshold (int): The threshold value for detecting changes in pixel intensity.
        kernel_size (tuple): The size of the Gaussian kernel used for blurring.
        sigma (float): The standard deviation of the Gaussian kernel.
        num_stack (int): The number of frames to stack.
        env (gym.Env): The wrapped environment.
        stack (collections.deque): A deque to store the stacked frames.
        shape (tuple): The shape of the observation space.
        observation_space (gym.spaces.Box): The modified observation space.

    Methods:
        create_grayscale(image): Converts an image to grayscale.
        gaussianDiff(previous, current): Computes the difference between two images using Gaussian blur.
        observation(obs): Performs the DVS transformation on the observation.
        threshold(change): Applies a threshold to the change map.
        reset(**kwargs): Resets the environment and returns the initial observation.

    """

    def __init__(self, env, change_threshold=60, kernel_size=(3, 3), sigma=1 ):
        super().__init__(env)
        
        self.change_threshold = change_threshold
        self.kernel_size = kernel_size
        self.sigma = sigma
        self.num_stack = 2 ## default
        self.env = gym.wrappers.FrameStack(env,self.num_stack)
        self.stack = collections.deque(maxlen=self.num_stack)
        
        stack, width, height, channels = self.env.observation_space.shape
        self.shape=(1, width, height)
        self.observation_space = gym.spaces.Box(shape=self.shape, low=0, high=255, dtype=np.uint8)
        
        print("In dvs wrapper")
        
    def create_grayscale(self, image):
        """
        Converts an image to grayscale.

        Args:
            image (numpy.ndarray): The input image.

        Returns:
            numpy.ndarray: The grayscale image.

        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        

    def gaussianDiff(self, previous, current):
        """
        Computes the difference between two images using Gaussian blur.

        Args:
            previous (numpy.ndarray): The previous image.
            current (numpy.ndarray): The current image.

        Returns:
            numpy.ndarray: The difference map.

        """
        previous = cv2.GaussianBlur(previous, self.kernel_size, self.sigma)
        np_previous = np.asarray(previous, dtype=np.int64)
        
        current = cv2.GaussianBlur(current, self.kernel_size, self.sigma)
        np_current = np.asarray(current, dtype=np.int64)
        
        change = np_current - np_previous
        
        return change.reshape(change.shape[0],change.shape[1],1)
    
    
    def observation(self, obs):
        """
        Performs the DVS transformation on the observation.

        Args:
            obs (list): The list of stacked frames.

        Returns:
            numpy.ndarray: The transformed observation.

        """
        prev = self.create_grayscale(obs[0])
        current = self.create_grayscale(obs[1])
        change = self.gaussianDiff(prev, current)
        
        ## threshold
        dc = self.threshold(change)
        
        return np.swapaxes(dc, 2, 0).astype(np.uint8)

    def threshold(self, change):
        """
        Applies a threshold to the change map.

        Args:
            change (numpy.ndarray): The change map.

        Returns:
            numpy.ndarray: The thresholded change map.

        """
        dc = np.ones(shape=change.shape) * 128
        dc[change >= self.change_threshold] = 255
        dc[change <= -self.change_threshold] = 0
        return dc
    
    
    def reset(self, **kwargs):
        """
        Resets the environment and returns the initial observation.

        Args:
            **kwargs: Additional keyword arguments for resetting the environment.

        Returns:
            numpy.ndarray: The initial observation.

        """
        obs, info = self.env.reset(**kwargs)
        
        frames = []
        [frames.append(obs) for _ in range(self.num_stack)]
        return self.observation(frames)
    
    
        