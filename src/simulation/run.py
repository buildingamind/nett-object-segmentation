import json
import os

import yaml
import hydra
from omegaconf import DictConfig, OmegaConf, open_dict
import pdb
import pprint
from utils import omegaconf_to_dict
import torch

import common.base_agent as base_agent

from agent.supervised_agent import SupervisedAgent
from agent.unsupervised_agent import ICMAgent
from common.base_experiment import Experiment
from env_wrapper.parsing_env_wrapper import ParsingEnv
import common.logger as logger
from GPUtil import getFirstAvailable

class ParsingExperiment(Experiment):
    """
    Class contains code for parsing experiment.

    Args:
        Experiment (class): Base class for experiments.

    Attributes:
        config (dict): Configuration parameters for the experiment.

    Methods:
        generate_environment: Generates an environment based on the given configuration.
        generate_mode_parameter: Generates a mode parameter based on the given mode and environment configuration.
        new_agent: Creates a new agent based on the given configuration.
        generate_log_title: Generates a log title based on the environment configuration.

    """

    def __init__(self, config):
        super().__init__(config)

    def generate_environment(self, env_config):
        """
        Generates an environment based on the given configuration.

        Args:
            env_config (dict): A dictionary containing the configuration parameters for the environment.

        Returns:
            ParsingEnv: An instance of the ParsingEnv class representing the generated environment.

        """
        env = ParsingEnv(**env_config)
        return env

    def generate_mode_parameter(self, mode, env_config):
        """
        Generates a mode parameter based on the given mode and environment configuration.

        Args:
            mode (str): The mode to be included in the parameter.
            env_config (dict): The environment configuration containing the background and use_ship information.

        Returns:
            str: The generated mode parameter.
        """
        object = "ship" if env_config["use_ship"] else "fork"
        return f"{mode}-{env_config['background']}-{object}"

    def new_agent(self, config):
        """
        Creates a new agent based on the given configuration.

        Args:
            config (dict): Configuration parameters for the agent.

        Returns:
            SupervisedAgent or ICMAgent: An instance of the agent based on the configuration.
        """
        
        if config["reward"].lower() == "supervised":
            return SupervisedAgent(**config)

        return ICMAgent(**config)

    def generate_log_title(self, env_config):
        """
        Generates a log title based on the environment configuration.

        Args:
            env_config (dict): Environment configuration data.

        Returns:
            str: Computed log title.
        """
        object = "ship" if env_config["use_ship"] else "fork"
        return "-".join(["_".join([object, env_config["background"]]), env_config["run_id"]])
    
    
@hydra.main(version_base=None, config_path="conf",
            config_name="config")
def run_experiment(cfg: DictConfig):
    with open_dict(cfg):
        print(cfg)
    
    #configuration= omegaconf_to_dict(cfg)
    ve = ParsingExperiment(cfg)
    ve.run()
    
    

if __name__ == '__main__':
    run_experiment()
