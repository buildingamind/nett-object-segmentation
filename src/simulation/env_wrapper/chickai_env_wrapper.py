from abc import ABC, abstractmethod
from pprint import pprint
from typing import Optional

import gym

from mlagents_envs.environment import UnityEnvironment
from gym_unity.envs import UnityToGymWrapper

from common.logger import Logger
from env_wrapper.dvs_wrapper import DVSWrapper
from env_wrapper.observation_wrapper import StitchVisualObservationsWrapper
from utils import port_in_use
import pdb

class ChickAIEnvWrapper(gym.Wrapper):
    """
    Wrapper class for the ChickAI environment.

    Args:
        run_id (str): The ID of the current run.
        env_path (str): The path to the Unity environment executable.
        base_port (int): The base port number for the Unity environment.
        **kwargs: Additional keyword arguments.

    Attributes:
        env (UnityToGymWrapper): The wrapped Unity environment.
        mode (str): The mode of the environment.

    Methods:
        step: Step the environment for one timestep.
        log: Write to the log file.
        close: Close the environment.
        reset: Reset the environment.
        steps_from_eps: Get the number of steps from the given episode.

    """

    def __init__(self, run_id: str, env_path=None, base_port=5004, **kwargs):
        """
        Initialize the ChickAIEnvWrapper.

        Args:
            run_id (str): The ID of the current run.
            env_path (str): The path to the Unity environment executable.
            base_port (int): The base port number for the Unity environment.
            **kwargs: Additional keyword arguments.

        """
        # Parse arguments and determine which version of the environment to use.
        args = self._parse_arguments(kwargs)

        # Find unused port
        while port_in_use(base_port):
            base_port += 1

        # Create logger
        self.log = self._create_logger(run_id=run_id, kwargs=kwargs)

        # Create environment and connect it to logger
        env = UnityEnvironment(env_path, side_channels=[self.log], additional_args=args, base_port=base_port)
        twoeyed = kwargs['twoeyed']
        if not twoeyed:
            self.env = UnityToGymWrapper(env, uint8_visual=True)
        else:
            env = UnityToGymWrapper(env, uint8_visual=True, allow_multiple_obs=True)
            self.env = StitchVisualObservationsWrapper(env)


        if "dvs_wrapper" in kwargs and kwargs["dvs_wrapper"]:
            self.env = DVSWrapper(self.env)
        
        super().__init__(self.env)

    def _parse_arguments(self, kwargs):
        """
        Parse the keyword arguments and convert them to Unity command line arguments.

        Args:
            kwargs: Additional keyword arguments.

        Returns:
            list: The parsed command line arguments.

        """
        args = []
        if "rec_path" in kwargs:
            args.extend(["--log-dir", kwargs["rec_path"]])
        if "recording_frames" in kwargs:
            args.extend(["--recording-steps", str(kwargs["recording_frames"])])
        if "record_chamber" in kwargs and kwargs["record_chamber"]:
            args.extend(["--record-chamber", "true"])
        if "record_agent" in kwargs and kwargs["record_agent"]:
            args.extend(["--record-agent", "true"])
        if "random_pos" in kwargs:
            args.extend(["--random-pos", "true"])
        if "rewarded" in kwargs:
            args.extend(["--rewarded", "true" if kwargs["rewarded"] else "false"])
        if "episode_steps" in kwargs:
            args.extend(["--episode-steps", str(kwargs['episode_steps'])])
        if "mode" in kwargs:
            args.extend(["--mode", kwargs["mode"]])
            self.mode = kwargs["mode"]
        else:
            self.mode = "rest"
        return args

    def _create_logger(self, run_id, kwargs):
        """
        Create a logger for the environment.

        Args:
            run_id (str): The ID of the current run.
            kwargs: Additional keyword arguments.

        Returns:
            Logger: The created logger.

        """
        log_title = kwargs.get("log_title", run_id)
        return Logger(log_title, log_dir=kwargs["log_path"])

    def step(self, action):
        """
        Step the environment for one timestep.

        Args:
            action: The action to take in the environment.

        Returns:
            tuple: A tuple containing the next state, reward, done flag, and additional information.

        """
        next_state, reward, done, info = self.env.step(action)
        return next_state, float(reward), done, info

    def log(self, msg: str) -> None:
        """
        Write a message to the log file.

        Args:
            msg (str): The message to write.

        Returns:
            None

        """
        self.log.log_str(msg)

    def close(self):
        """
        Close the environment.

        Returns:
            None

        """
        self.env.close()
        del self.log

    def reset(self, seed: Optional[int] = None, **kwargs):
        """
        Reset the environment.

        Args:
            seed (int): The random seed for the environment.
            **kwargs: Additional keyword arguments.

        Returns:
            The initial state of the environment.

        """
        # nothing to do if the wrapped env does not accept `seed`
        return self.env.reset(**kwargs)

    @abstractmethod
    def steps_from_eps(self, eps):
        """
        Get the number of steps from the given episode.

        Args:
            eps: The episode.

        Returns:
            int: The number of steps.

        """
        pass
    