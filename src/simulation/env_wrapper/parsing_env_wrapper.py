
#!/usr/bin/env python3

from env_wrapper.chickai_env_wrapper import ChickAIEnvWrapper



class ParsingEnv(ChickAIEnvWrapper):
    """
    A class representing the Parsing Environment.

    Attributes:
        numb_conditions (int): The number of test conditions in the environment.

    Methods:
        __init__(self, run_id: str, env_path=None, base_port=5004, **kwargs): Initializes the ParsingEnv object.
        steps_from_eps(self, eps): Calculates the number of steps based on the number of episodes.
    """

    @property
    def numb_conditions(self):
        return 56
    
    def __init__(self, run_id: str, env_path=None, base_port=5004, **kwargs):
        super().__init__(run_id, env_path, base_port, **kwargs)
    
    def steps_from_eps(self, eps):
        """
        Calculates the number of steps based on the number of episodes.

        Args:
            eps (int): The number of episodes.

        Returns:
            int: The total number of steps.

        """
        step_per_episode = 200

        if "rest" in self.mode:
            return step_per_episode * eps
        
        return step_per_episode * eps * self.numb_conditions
    