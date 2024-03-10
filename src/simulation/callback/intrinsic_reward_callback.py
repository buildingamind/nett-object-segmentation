#!/usr/bin/env python3

from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.on_policy_algorithm import OnPolicyAlgorithm
from stable_baselines3.common.callbacks import BaseCallback


import torch as th

class IntrinsicRewardCallback(BaseCallback):
    def __init__(self, irs, verbose = 0):
        """_summary_

        Args:
            irs (_type_): _description_
            verbose (int, optional): _description_. Defaults to 0.
        """
        super(IntrinsicRewardCallback, self).__init__(verbose)
        self.irs = irs
        self.verbose = verbose
        self.buffer = None
        
    def init_callback(self, model: BaseAlgorithm) -> None:
        """_summary_

        Args:
            model (BaseAlgorithm): _description_
        """
        super().init_callback(model)
        if isinstance(self.model, OnPolicyAlgorithm):
            self.buffer = self.model.rollout_buffer
            
    def _on_step(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        observations = self.locals["obs_tensor"]
        self.device = observations.device
        actions = th.as_tensor(self.locals["actions"], device=self.device)
        rewards = th.as_tensor(self.locals["rewards"], device=self.device)
        dones = th.as_tensor(self.locals["dones"], device=self.device)
        next_observations = th.as_tensor(self.locals["new_obs"], device=self.device)
        
        return True
    
    def _on_rollout_end(self) -> None:
        """_summary_"""
        obs = th.as_tensor(self.buffer.observations, device=self.device)
        actions = th.as_tensor(self.buffer.actions, device=self.device)
        rewards = th.as_tensor(self.buffer.rewards, device=self.device)
        dones = th.as_tensor(self.buffer.episode_starts, device=self.device)
        intrinsic_rewards = self.irs.compute_irs(samples=dict(observations=obs, 
                                                     actions=actions, 
                                                     rewards=rewards, 
                                                     terminateds=dones,
                                                     truncateds=dones, 
                                                     next_observations=obs
                                                     ))
        
        print(intrinsic_rewards)
        self.buffer.advantages += intrinsic_rewards.cpu().numpy()
        self.buffer.returns += intrinsic_rewards.cpu().numpy()
        