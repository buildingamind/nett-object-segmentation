#!/usr/bin/env python3

from abc import ABC, abstractmethod
import os
from typing import Optional

import torch
from gym.wrappers.monitoring.video_recorder import VideoRecorder

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common import results_plotter


import matplotlib.pyplot as plt
import numpy as np
from sb3_contrib import RecurrentPPO
from tqdm import tqdm

from utils import debug_logger, to_dict, write_to_file
from networks.encoder_config import ENCODERS
from GPUtil import getFirstAvailable


class BaseAgent(ABC):
    def __init__(self, agent_id="Default Agent", \
        log_path="./Brains",
        **kwargs):
        
        self.id = agent_id
        self.model = None
        self.summary_freq = 30000 
        self.rec_path = kwargs['rec_path'] if 'rec_path' in kwargs else ""
        
        ## get encoder configuration
        encoder = kwargs.get('encoder', {})
        self.encoder_type = encoder.get('name', '')
        if self.encoder_type not in ENCODERS:
            raise ValueError(f"Encoder type '{self.encoder_type}' not found in encoder_config file.")
        self.encoder = ENCODERS[self.encoder_type]['encoder']
        self.encoder_dim = ENCODERS[self.encoder_type]['feature_dimensions']
        self.train_encoder = encoder.get('train',True)
        
        ## get other parameters
        self.batch_size = kwargs['mini_batchsize']
        self.buffer_size = kwargs['buffer_size']
        self.seed = kwargs['seed']
        
        ## set device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.policy = kwargs["policy"]

        # If path does not exist, create it as a directory
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.log_dir = log_path

        if os.path.isfile(log_path):
            self.path = log_path
        else:
            self.path = os.path.join(log_path, self.id)

        self.plots_path = os.path.join(self.path , "plots")
        os.makedirs(self.plots_path, exist_ok = True)

        self.env_log_path = kwargs['env_log_path']
        self.model_save_path = os.path.join(self.path, "model")

        ## recordings path - recordings
        self.video_record_path = os.path.join(self.rec_path,"test")
        os.makedirs(self.video_record_path, exist_ok=True)

        ## set cuda device if available
        self.device_num = getFirstAvailable(attempts=5, interval=5, maxMemory=0.5, verbose=True)
        print(self.device_num)
        torch.cuda.set_device(self.device_num[0])
        assert torch.cuda.current_device() == self.device_num[0]

        self.debug_logger = debug_logger(os.path.join(self.path, "agent.log"))
        self.object_background = kwargs.get("env_object_background","")

        
    @abstractmethod   
    def train(self, env, eps)->None:
        pass

    def test(self, env, eps, record_prefix = "rest"):
        """
        Test the agent in the given environment for the set number of steps

        Args:
            env : gym environment wrapper
            eps : number of test episodes
            record_prefix (str, optional): recording file name prefix
        """
        self.load()
        if self.model == None:
            self.debug_logger.error("Usage Error: model is not specified either train a new model or load a trained model")
            return
        
        #Run the testing
        steps = env.steps_from_eps(eps)
        
        e_gen = lambda : env
        envs = make_vec_env(env_id=e_gen, n_envs=1)
        
        ## record - test video
        vr = VideoRecorder(env=envs,
        path="{}/{}_{}.mp4".format(self.video_record_path, \
            str(self.id), record_prefix), enabled=True)
        
        
        if self.policy.lower()=="ppo":
            self.debug_logger.info(f"Total number of steps:{steps}")
            obs = envs.reset()
            for i in tqdm(range(steps), desc="Testing progress"):
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = envs.step(action)
                
                if done:
                    env.reset()
                
                env.render(mode="rgb_array")
                vr.capture_frame()    

            vr.close()
            vr.enabled = False
            
        else:
            total_number_of_episodes = env.total_number_of_test_eps(eps)
            self.debug_logger.info(total_number_of_episodes)
            num_envs = 1
            for i in tqdm(range(total_number_of_episodes), desc="Testing progress"):
                obs = env.reset()
                # cell and hidden state of the LSTM
                dones, lstm_states = False, None
                num_envs = 1

                # Episode start signals are used to reset the lstm states
                episode_starts = np.ones((num_envs,), dtype=bool)
                episode_length = 0
                while not dones:
                    action, lstm_states = self.model.predict(obs, state=lstm_states, episode_start=episode_starts, deterministic=True)
                    obs, rewards, dones, info = env.step(action)
                    episode_starts = dones
                    episode_length += 1
                    env.render(mode="rgb_array")
                    vr.capture_frame()    
                    
                #print(f"Episode length:{episode_length}, num_episode = {i}")
                    
            vr.close()
            vr.enabled = False          
            
        del self.model
        self.model = None
    
    def save(self, path: Optional[str] = None) -> None:
        """
        Save agent prains to the specified path

        Args:
            path (str): Path value to save the model
        """
        if path is None:
            path = self.model_save_path
        
        if self.model == None:
            self.load(path)
        else:
            self.model.save(path)
    
    def load(self, path=None)->None:
        """
        Load the model from the specified path

        Args:
            path (str): model saved path. Defaults to None.
        """
        self.debug_logger.info("load called")
        if path == None:
            path = self.model_save_path
        
        self.debug_logger.info(self.model_save_path)
        if self.policy.lower() == "ppo":
            self.model = PPO.load(self.model_save_path, print_system_info=True)
        else:
            self.debug_logger.info("Loading recurrent agent:" + self.model_save_path)
            self.model = RecurrentPPO.load(self.model_save_path, print_system_info=True)
        
    def check_env(self, env):
        """
        Check environment

        Args:
            env (vector environment): vector env check for correctness

        Raises:
            Exception: raise exception if env check fails

        Returns:
            bool: env check is successful or failed
        """
        env_check = check_env(env, warn=True)
        if env_check != None:
            self.debug_logger.error(f"Failed env check: {str(ex)}")
            raise Exception(f"Failed env check")
        
        return True

    def plot_results(self, steps:int, plot_name="chickai-train") -> None:
        """
        Generate reward plot for training

        Args:
            steps (int): number of training steps
            plot_name (str, optional): Name of the reward plot. Defaults to "chickai-train".
        """
        results_plotter.plot_results([self.path], steps, 
                                     results_plotter.X_TIMESTEPS, plot_name)
        
        
        plt.savefig(self.plots_path + "/" + plot_name + ".png")
        plt.clf()
        
    def save_encoder_policy_network(self):
        """
        Saves the policy and feature extractor of the agent's model.

        This method saves the policy and feature extractor of the agent's model
        to the specified paths. It first checks if the model is loaded, and if not,
        it prints an error message and returns. Otherwise, it saves the policy as
        a pickle file and the feature extractor as a PyTorch state dictionary.

        Returns:
            None
        """
        self.load()
        if self.model == None:
            self.debug_logger.error("Usage Error: model is not specified either train a new model or load a trained model")
            return
        
        base_path, model_name = os.path.split(self.model_save_path)
        
        ## save policy
        policy = self.model.policy
        policy.save(os.path.join(base_path, "policy.pkl"))
        
        ## save encoder
        encoder = self.model.policy.features_extractor.state_dict()
        save_path = os.path.join(base_path, "feature_extractor.pth")
        torch.save(encoder, save_path)
        
        self.debug_logger.info(f"Saved feature_extractor: {save_path}")
        return
    
    def set_feature_extractor_require_grad(self, model):
        """
        Sets the `requires_grad` attribute of the parameters in the feature extractor of the given model to False.
        
        Args:
            model (torch.nn.Module): The model whose feature extractor parameters need to have `requires_grad` set to False.
        
        Returns:
            torch.nn.Module: The updated model with feature extractor parameters having `requires_grad` set to False.
        """
        model.policy.features_extractor.eval()
        for param in model.policy.features_extractor.parameters():
            param.requires_grad = False
            
        return model
    
    def write_model_properties(self, model, steps):
        """
        Writes the properties of the model to a JSON file.

        Args:
            model (object): The model object.
            steps (int): The total number of timesteps.

        Returns:
            None
        """
        model_props = {
            "encoder_type": self.encoder_type,
            "batch_size": self.batch_size,
            "buffer_size": self.buffer_size,
            "policy": self.policy,
            "total_timesteps": steps,
            "tensorboard_path": self.path,
            "logpath": self.path,
            "agent_id": self.id
        }

        model_dict = to_dict(model.__dict__)
        model_dict.update(model_props)

        file_path = os.path.join(self.path, "model_agent_dump.json")
        write_to_file(file_path, model_dict)