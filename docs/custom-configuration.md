## Custom Configurations

1. **Modifying the Agent's Brain**: After having replicated the results with the default configuration, you may wish to experiment by plugging in different brains for the agent. We have included a few different possible brains for the agent. To plug these in simply modify the `yaml` file in `src/simulation/conf/Agent/basic.yaml`.

```yaml
encoder:
  name: BRAIN
  train: True

```

Note that if you change the size of the encoder, you may also consider changing the number of training episodes. This can be done in the config file `src/simulation/conf/config.yaml`.

```
train_eps: NEW_EPISODE_COUNT
```

2. **Modifying the Policy Network**: The policy network can be modified by updating 'policy' in src/simulation/conf/Agent/basic.yaml. The available options are PPO and LSTM (recurrent policy).

```
policy: POLICY_NAME
```
Replace POLICY_NAME with either PPO or LSTM depending on your preference. Remember to save the changes in the yaml files after modifying them. The new configurations will be used the next time you run the simulation.

3. **DVS Wrapper**: To run experiments with the DVS Wrapper, you need to modify the `dvs_wrapper` value in the `src/simulation/conf/Environment/parsing.yaml` file. 

```yaml
dvs_wrapper: VALUE
```
Replace VALUE with either True or False depending on whether you want to enable or disable the DVS Wrapper. When dvs_wrapper is set to True, the DVS Wrapper will be used in the simulation. When it's set to False, the DVS Wrapper will not be used. Remember to save the changes in the yaml file after modifying it. The new configuration will be used the next time you run the simulation.


4. **Experiment Mode**: The mode of the experiment can be set in the `src/simulation/conf/config.yaml` file. 

```yaml
mode: MODE
```
Replace MODE with either full, train, or test depending on the mode you want to set for the experiment.

**full**: The experiment will complete both training and testing runs.
**train**: The experiment will only complete the training run.
**test**: The experiment will only complete the test run.


5. **Recording frames seen by the agent** Recording can be turned on by setting various flags in ```src/simulation/conf/Environment/parsing.yaml``` file
```
train_record_agent: TRAIN_AGENT_VALUE
train_record_chamber: TRAIN_CHAMBER_VALUE
test_record_agent: TEST_AGENT_VALUE
test_record_chamber: TEST_CHAMBER_VALUE
```
Replace TRAIN_AGENT_VALUE, TRAIN_CHAMBER_VALUE, TEST_AGENT_VALUE, and TEST_CHAMBER_VALUE with either True or False depending on whether you want to enable or disable frame recording.

True: The frames seen by the agent or the chamber will be recorded during the training or testing phase of the simulation.
False: The frames will not be recorded.
The recorded frames will be saved in a specified directory which can be set in the same file:

```
rec_path: ${log_path}/Recordings/
```
Following is the structure of the folder when all the flags are turned on.

```
├── Brains
│   └── parsing_ship_A_exp2_Agent_0
│       ├── best_performance_model.zip
│       ├── checkpoints
│       │   ├── supervised_model_120000_steps.zip
│       │   ├── supervised_model_150000_steps.zip
│       │   ├── supervised_model_180000_steps.zip
│       │   ├── supervised_model_30000_steps.zip
│       │   ├── supervised_model_60000_steps.zip
│       │   └── supervised_model_90000_steps.zip
│       ├── events.out.tfevents.1710036252.bear.2153142.0
│       ├── feature_extractor.pth
│       ├── model_agent_dump.json
│       ├── model.zip
│       ├── monitor.csv
│       ├── plots
│       │   └── reward_graph_parsing_ship_A_exp2_Agent_0.png
│       ├── policy.pkl
│       └── progress.csv
├── Env_Logs
│   ├── ship_A-parsing_ship_A_exp2_Agent_0_test.csv
│   └── ship_A-parsing_ship_A_exp2_Agent_0_train.csv
├── Recordings
│   └── parsing_ship_A_exp2_Agent_0
│       ├── test
│           ├── AgentRecorder
|           |    ├── Agent_1.png
|           |    ├── ..
|           |    ├── Agent_x.png
│           ├── ChamberRecorder
|           |    ├── Chamber_1.png
|           |    ├── ..
|           |    ├── Chamber_x.png
│           ├── parsing_ship_A_exp2_Agent_0_test.meta.json
│           └── parsing_ship_A_exp2_Agent_0_test.mp4
│       └── train
│           ├── AgentRecorder
|           |    ├── Agent_1.png
|           |    ├── ..
|           |    ├── Agent_x.png
│           └── ChamberRecorder
|           |    ├── Chamber_1.png
|           |    ├── ..
|           |    ├── Chamber_x.png
└── run.log
```


6. **Running Multiple Agents**: If you want to run more than one agent in the simulation, you can set this up in the `src/simulation/conf/config.yaml` file.

```yaml
agent_count: NUMBER_OF_AGENTS
```

7. **Running Two-Eyed Agents**: If you want to run agents with two eyes in the simulation, after download the executable in location: https://origins.luddy.indiana.edu/unity/iclr-2024/executables/parsing_stereo.zip and providing right permissions to the executable to run - refer README.md getting started section. Update the path to the executable in the ```src/simulation/conf/Environment/parsing.yaml```

```
env_path: data/executables/parsing_2eyedbenchmark/parsing.x86_64

```
and turn on the TwoEyed value in the agent config (```src/simulation/conf/Agent/basic.yaml```) to True. 

```yaml
TwoEyed: BOOLEAN_VALUE
```
True: The agents will have two eyes in the simulation.
False: The agents will have one eye in the simulation.

