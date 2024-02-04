import abc
import os
from omegaconf import open_dict
import common.base_agent as base_agent

class Experiment(abc.ABC):
    def __init__(self, config):
        self.env_config = config["Environment"]
        agent_config = config["Agent"]
        agent_count = config["agent_count"]
        
        run_id = config["run_id"]
        self.mode = config["mode"]
        
        self.reward = agent_config["reward"]
        self.rewarded = self.reward.lower() == "supervised"
        
        self.log_path = config["log_path"]
        self.test_eps = config["test_eps"]
        self.train_eps = config["train_eps"]
        self.agents = []

        for i in range(agent_count):
            with open_dict(agent_config):
                agent_config.agent_id = f"{run_id}_Agent_{i}"
                agent_config.env_log_path = self.env_config['log_path']
                agent_config.rec_path = os.path.join(self.env_config["rec_path"], agent_config.agent_id)
                agent_config.recording_frames = self.env_config["recording_frames"]
                agent_config.env_object_background = f"ship_{self.env_config['background']}" if self.env_config["use_ship"]  \
                    else f"fork_{self.env_config['background']}"
            self.agents.append(self.new_agent(agent_config))

    
    def train_agents(self):
        """
        Function to build training configuration, 
        generate environments and start training
        """
        for agent in self.agents:
            env_config = self.env_config
            with open_dict(env_config):
                mode = "rest"
                env_config["mode"] = self.generate_mode_parameter(mode,env_config)
                env_config["random_pos"] = True
                
                if self.rewarded:
                    env_config["rewarded"] = self.rewarded
                
                env_config["run_id"] = agent.id + "_" + "train"
                env_config["rec_path"] = os.path.join(agent.rec_path , "train", "/")    
                env_config["log_title"] = self.generate_log_title(env_config)
                
            
            env = self.generate_environment(env_config)
            agent.train(env, self.train_eps)
            agent.save()
            env.close()
    

    def test_agents(self,mode):
        for agent in self.agents:
            env_config = self.env_config
            with open_dict(env_config):
                
                env_config["mode"] = self.generate_mode_parameter(mode, env_config)
                env_config["run_id"] = agent.id + "_" + mode
                env_config["rec_path"] = os.path.join(agent.rec_path , "test", "/")

                if self.rewarded:
                    env_config["rewarded"] = self.rewarded
                env_config["reward"] = self.reward
                
                env_config["log_title"] = self.generate_log_title(env_config)
            env = self.generate_environment(env_config)
            agent.test(env, self.test_eps, mode)
            env.close()

    
    def run(self):
        if self.mode == "train":
            self.train_agents()
        elif self.mode == "test":
            self.test_agents("test")
        elif self.mode == "full":
            self.train_agents()
            self.test_agents("test")
        else:
            self.test_agents("test")

    @abc.abstractmethod
    def generate_environment(self, env_config):
        pass

    def new_agent(self, config):
        return base_agent.BaseAgent(**config)
    
    @abc.abstractmethod
    def generate_mode_parameter(self, mode, env_config):
        pass
        
    @abc.abstractmethod
    def generate_log_title(self, env_config):
        pass
    