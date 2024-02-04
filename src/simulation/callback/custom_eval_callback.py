#! /usr/bin/env python3
import os
import warnings
from typing import Any, Callable, Dict, List, Optional, Union
import glob
import gym
import numpy as np
from stable_baselines3.common.callbacks import BaseCallback, EventCallback,EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import (
    DummyVecEnv,
    VecEnv,
    sync_envs_normalization,
)
import shutil
import pdb


class CustomEvalCallback(EvalCallback):
    """
    Callback for evaluating an agent.

    
    :param eval_env: The environment used for initialization
    :param n_eval_episodes: The number of episodes to tests the agent
    :param eval_freq: Evaluate the agent every ``eval_freq`` call of the callback.
    :param log_path: Path to a folder where the evaluations (``evaluations.npz``)
        will be saved. It will be updated at each evaluation.
    :param deterministic: Whether the evaluation should
        use a stochastic or deterministic actions.
    :param render: Whether to render or not the environment during evaluation
    :param verbose:
    :param warn: Passed to ``evaluate_policy`` (warns if ``eval_env`` has not been
        wrapped with a Monitor wrapper)
    """

    def __init__(
        self,
        eval_env: gym.Env,
        n_eval_episodes: int = 5,
        eval_steps: int = 1120,
        env_log_path: str= "",
        eval_freq: int = 20000,
        deterministic: bool = True,
        verbose: int = 0,
        
    ):
        super().__init__(eval_env)
        
        self.eval_env = eval_env
        self.n_eval_episodes = n_eval_episodes
        self.eval_freq = eval_freq
        self.best_mean_reward = -np.inf
        self.deterministic = True
        self.render = False
        self.eval_steps = eval_steps
        self.env_log_path = env_log_path
        
        # Convert to VecEnv for consistency
        if not isinstance(eval_env, VecEnv):
            eval_env = DummyVecEnv([lambda: eval_env])

        self.eval_env = eval_env
        self.n_episodes = 0 

    

    def _on_step(self) -> bool:
        continue_training = True
        episode_rewards = []
        episode_lengths = []
        
        #print(f"n calls:{self.n_calls} and {self.eval_freq}")
        
        if self.eval_freq > 0 and self.n_calls % self.eval_freq == 0:
            n_envs =1
            current_rewards =0
            current_lengths = 0
            print("Evaluating the policy")
            obs = self.eval_env.reset()
            for i in range(self.eval_steps):
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.eval_env.step(action)
                current_rewards += reward
                current_lengths += 1
                
                if done:
                    episode_rewards.append(current_rewards)
                    episode_lengths.append(current_lengths)
                    current_rewards = 0
                    current_lengths = 0
                    self.eval_env.reset()
                    
            mean_reward = np.mean(episode_rewards)
            std_reward = np.std(episode_rewards)
            print(f"Mean reward: {mean_reward:.2f}, std reward:  {std_reward:.2f}")
            
            ## end of evaluation move the env_log into evaluation folder and rename based on n_calls
            try:
                eval_files = glob.glob(os.path.join(self.env_log_path, "*test_eval.csv"))
                if len(eval_files) == 0:
                    raise Exception(f"Training file: {eval_files} was not found in the {self.env_log_path}")
        
                eval_file_name = eval_files.pop()
                name = os.path.splitext(os.path.basename(eval_file_name))[0]
                shutil.copy(eval_file_name, os.path.join(self.env_log_path, f"{name}_{self.n_calls}.csv"))

            except Exception as e:
                print("exeception occurred while renaming the file")

        return continue_training
