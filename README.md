<div align="center">

# A NEWBORN EMBODIED TURING TEST FOR COMPARING OBJECT SEGMENTATION ACROSS ANIMALS AND MACHINES
 Manjulata Garimella, Denizhan Pak, Justin N. Wood, Samantha M. W. Wood 

  [Paper](https://openreview.net/pdf?id=qhkEOCcVX9)
| [Dataset](https://origins.luddy.indiana.edu/unity/iclr-2024/)
| [Lab Website](http://buildingamind.com/) 
| [Getting Started](#getting-started) 
| [Documentation](https://buildingamind.github.io/nett-object-segmentation/) 
![GitHub License](https://img.shields.io/github/license/buildingamind/nett-object-segmentation)

</div>

## Abstract

Newborn brains rapidly learn to solve challenging object perception tasks, including segmenting objects from backgrounds and recognizing objects across new viewing situations. Conversely, modern machine learning (ML) algorithms are “data hungry,” requiring more training data than brains to reach similar performance levels. How do we close this learning gap between brains and machines? Here, we introduce a new benchmark—a Newborn Embodied Turing Test (NETT) for object segmentation—in which newborn animals and machines are raised in the same environments and tested with the same tasks, permitting direct comparison of their learning. First, newborn chicks were raised in controlled environments containing a single object rotating on a single background, then their recognition performance was tested across new backgrounds and viewpoints. Second, we performed “digital twin” experiments in which artificial agents were reared and tested in virtual environments that mimicked the rearing and testing conditions of the chicks. We inserted a variety of ML “brains” into the artificial agents and measured whether those algorithms learned common object recognition behavior as chicks. All newborn chicks solved this one-shot object segmentation task, successfully learning *background-invariant* object representations that generalized across new backgrounds and viewpoints. In contrast, none of the artificial agents solved the task, instead learning *background-dependent* representations that failed to generalize across new backgrounds and viewpoints. This digital twin design exposes core limitations in current ML algorithms in developing brain-like object perception. Our NETT is publicly available for comparing ML algorithms with newborn chicks. We argue that NETT benchmarks can help researchers build embodied AI systems that learn as efficiently and robustly as newborn brains.

Below is a visual representation of our experimental setup, showcasing the infrastructure for the three primary experiments discussed in this documentation.

<div align="center">
  <img src="https://github.com/buildingamind/nett-object-segmentation/blob/main/docs/_static/figure1.jpg" alt="nett_architecture"/>
</div>


## **How to Use this Repository**

The repository comprises three key components:

1. **Virtual Environment**: A dynamic environment that serves as the habitat for virtual agents.
2. **Experimental Simulation Programs**: Tools to initiate and conduct experiments within the virtual world.
3. **Data Visualization Programs**: Utilities for analyzing and visualizing experiment outcomes.

If users are unfamiliar with how to install a git repository or have never used unity before please scroll down to how to the [How to install](#how-to-install)

## **Directory Structure**

**Following the directory structure of the code.**

```
.
├── docs                     # Documentation and guides
├── data										 # Placeholder to storing executables, runs and checkpoints
│   ├── checkpoints 
│   │   └── simclr
│   ├── executables
│   │   ├── parsing_benchmark2eyed
│   │   └── parsing_benchmark
│   └── runs
├── LICENSE									 # License file
├── README.md								 # Readme file
├── requirements.txt				 # requirements.txt file containing project requirements
├── scripts									 # Example scripts for running experiments
│   └── parsing_sup.sh
├── setup.cfg
├── src										     # Folder containing src code
│   ├── analysis							 # Folder containing R-scripts for doing analysis
│   │   ├── r														
│   │   └── README.md
│   └── simulation						 # Folder containing simulation code for experiments
│       ├── agent							 # Agent configuration
│       ├── algorithms					 # Algorithms - like Intrinsic curiosity module
│       ├── callback						 # Callback functions to compute metrics during training
│       ├── common						 # Common function
│       ├── conf							 # Hydra configuration for running experiments
│       ├── env_wrapper					 # Environment wrapper 
│       ├── GPUtil.py					 # GPUUtils functions
│       ├── networks					 # Encoders models
│       ├── run.py             # Main file to run experiment
│       └── utils.py					 # Utility functions
└── tests									     # pytests folder
    ├── pytest.ini		
    └── test_env.py

```
## Getting Started

The section describes how to get started with running the experiments and performing the analysis of the results.

### Installation

## How to Install

This section describes the installation of simulation code and running the benchmark experiments.

### Downloading Unity Assets

The first step is downloading unity executable. The unity executables can be downloaded from:

| Unity Executable  | Link |
| ------------- | ------------- |
| Parsing  | https://origins.luddy.indiana.edu/unity/iclr-2024/executables/parsing.zip    |
| Parsing Stereo (2-eyed agent)  | https://origins.luddy.indiana.edu/unity/iclr-2024/executables/parsing_stereo.zip     |
 
After downloading the execuatable run following commands to unzip and copy into executables folder in data

```
mkdir data
cd data
mkdir executables
unzip <name_of_executable>
mv <name_of_executable> executables/.
```
Ensure there is following directory structure
```
.
└── data/
    └── executables/
        ├── <exp_name>/
        │   └── <build_artifcats>
        ├── <exp_name>/
        │   └── <build_artifacts>
        ├── .
        ├── .
        └── <exp_name>/
            └── <build_artifacts>
```

The next step is to give executable 755 permissions, as shown below. For example:

```
chmod -R 755 data/executables/parsing/parsing.x86_64
```

After this step, run 
```
nvidia-smi
```
This will show you if anyone else is running on the server, and if so, what GPUs they are using. It will also show you if the X Server is running. The X server acts as a virtual display (so that the game isn't played "headless.") If the X Server is running correctly, the bottom "processes" table will show "/usr/lib/xorg/Xorg" for every GPU. If you don't see the Xorg process, then the X Server needs to be restarted. The command to restart the server is below, but note that you'll need sudo privileges to restart the X Server

```
sudo /usr/bin/X :0 
```

Make Ubuntu use X Server for display.

```
export DISPLAY=:0
```

### Downloading Pretrained Models
In order, to run pretrained SIMCLR experiments download the model state dict from:[SIMCLR](https://origins.luddy.indiana.edu/unity/iclr-2024/checkpoints/simclr). Copy the checkpoints into - data/checkpoints folder. The new directory structure show look like this:
```
├── data
│   ├── checkpoints
│   │   └── simclr
│   │       ├── fork_A
│   │       ├── fork_B
│   │       ├── fork_C
│   │       ├── ship_A
│   │       ├── ship_B
│   │       └── ship_C
│   ├── executables
│   │   └── parsing_benchmark
│   │       ├── parsing_Data
│   │       ├── parsing.x86_64
│   │       └── UnityPlayer.so
│   └── runs
```

### Codebase Installation

1. **Install Git and/or Github Desktop**: If you install Git, you'll be able to interact with Github through the command line. You can download Git using the directions here: [https://git-scm.com/downloads](https://git-scm.com/downloads). If you install Git Desktop, you can use a GUI to interact with Github. You can install Github Desktop by following the directions here: [https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/). For the following steps, I will provide the command line arguments (but you can use the GUI to find the same options in Github Desktop).

2. To download the repository, click the Code button on the nett-object-segmentation repo. Copy the provided web URL. Then follow the code below to change to directory where you want the repo (denoted here as MY_FOLDER) and then clone the repo.
   ```
   cd MY_FOLDER
   git clone git@github.com:buildingamind/nett-object-segmentation.git

   ```
   
3. **Virtual Environment Setup** (Highly Recommended): Create and activate a virtual environment to avoid dependency conflicts.
   ```bash
   conda create -y -n nett_env python=3.8.17
   conda activate nett_env
   ```
   See [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda "Link for how to set-up a virtual env") for detailed instructions.

5. Install the needed versions of `setuptools` and `pip`:
   ```bash
   pip install setuptools==65.5.0 pip==21 
   ```
   **NOTE:** This is a result of incompatibilities with the subdependency `gym==0.21`. More information about this issue can be found [here](https://github.com/openai/gym/issues/3176#issuecomment-1560026649)

3. **Installation for other dependency**: Install the dependency using `pip`.
   ```bash
   pip install -r requirements.txt
   ```

Please check (#known-issues) to address known issues during installation.

### Running an Experiment (default configuration)

After having followed steps above experiments can be run with a few lines of code in the script

```
  bash scripts/parsing_sup.sh
```
or

```
python src/simulation/run.py

```

Once the experiment starts running you will see folder with <run_id> gets created based on the path specified in ```src/simulation/conf/config.yaml```
```
agent_count: 1
run_id: parsing_ship_A_exp1
log_path: data/runs/${run_id}
mode: full
train_eps: 1000
test_eps: 20
hydra.job.chdir: True
experiment: parsing

defaults:
  - _self_
  - Agent: basic
  - Environment: parsing
  - hydra
```
The structure of the folder
```
.
└── parsing_ship_A_exp1
    ├── Brains
    │   └── parsing_ship_A_exp1_Agent_0
    │       ├── checkpoints
    │       ├── events.out.tfevents.1710031706.bear.2140391.0
    │       ├── model_agent_dump.json
    │       ├── monitor.csv
    │       ├── plots
    │       └── progress.csv
    ├── Env_Logs
    │   └── ship_A-parsing_ship_A_exp1_Agent_0_train.csv
    ├── Recordings
    │   └── parsing_ship_A_exp1_Agent_0
    │       └── train
    |       └── test
    └── run.log
```
The experiments can be run on two objects with three backgrounds each (A, B and, C) as described in the paper:
Object 1 - Ship
Object 2 - Fork

The following code snippet shows how to update the configuration in `src/simulation/conf/Environment/parsing.yml` to run the experiment:

```yaml
use_ship: True
background: A
```

The configuration varies depending on the object:

- For Object 1: use_ship is set to true and background can be A, B, or C.
- For Object 2: use_ship is set to false and background can also be A, B, or C.
Refer to the videos below for a visual representation of these configurations.

| Object | Background A | Background B | Background C |
| ------ | ------------ | ------------ | ------------ |
| 1  (Ship)    | <img src="docs/_static/video/1A_00.gif" width="100" height="100" /> <br> | <img src="docs/_static/video/1B_00.gif" width="100" height="100" />  | <img src="docs/_static/video/1C_00.gif" width="100" height="100" />  |
| 2   (Fork)   | <img src="docs/_static/video/2A_00.gif" width="100" height="100" />  | <img src="docs/_static/video/2B_00.gif" width="100" height="100" />  | <img src="docs/_static/video/2C_00.gif" width="100" height="100" />  |



### Running Standard Analysis

After running the experiments, the pipeline will generate a collection of datafiles in the `data/runs` folder. To run the analyses performed in the papers you can use the following command

```
python3 src/analysis/r/run_analysis.py --log-dir data/runs
```

This will generate a collection of graphs in the folder `data/runs`.


### Running an Experiment (custom configuration)

Please refer following documentation if you wish to experiment plugging different configurations of the brain, policy and modify other environment parameters. [Custom Configuration](docs/custom-configuration.md)

### Miscellaneous

We have also implemented Unsupervised algorithms like Intrinsic Curiosity Module (ICM). If you would like to turn off, reward from the environment and use custom reward please update reward configuration in the agent config file - ```src/simulation/conf/Agent/basic.yaml```

```
reward: ICM

```


### Known Issues

#### Errors during installation

1. Issue with completing pip install due to torch version mismatch. This can be resolved by manually installing stable-baselines3, stable-baselines3[extra] and sb3_contrib later after pip install in step 3. 

```
pip install stable-baselines3==1.8
pip install stable-baselines3[extra]==1.8.0
pip install sb3_contrib==1.8
``` 
##### Errors during running the code

1. torch._six not found.

```
File "/home/<user>/anaconda3/envs/nett_env/lib/python3.8/site-packages/pl_bolts/datamodules/async_dataloader.py", line 7, in <module>
    from torch._six import container_abcs, string_classes
ModuleNotFoundError: No module named 'torch._six'
```
open the 'async_dataloader.py' in 'vi' and comment the line in the error.

```
File "/home/<user>/anaconda3/envs/nett_env2/lib/python3.8/site-packages/pl_bolts/datasets/imagenet_dataset.py", line 12, in <module>
    from torch._six import PY3
ModuleNotFoundError: No module named 'torch._six'
```
open the file `imagenet_dataset.py` and comment the line.

## Contributors
<table>
  <tr>
    <td align="center"><a href="https://github.com/mchivuku"><img src="https://avatars.githubusercontent.com/u/90662028?v=4?s=100" width="100px;" alt=""/><br /><b>Manjulata Garimella</b></td>
    <td align="center"><a href="https://github.com/denizhanpak"><img src="https://avatars.githubusercontent.com/u/90662028?v=4?s=100" width="100px;" alt=""/><br /><b>Denizhan Pak</b></td>
    <td align="center"><a href="https://github.com/smwwood"><img src="https://avatars.githubusercontent.com/u/90662028?v=4?s=100" width="100px;" alt=""/><br /><b> Samantha M. W. Wood</b></td>
    <td align="center"><a href="https://github.com/justinnwood"><img src="https://avatars.githubusercontent.com/u/90662028?v=4?s=100" width="100px;" alt=""/><br /><b> Justin N. Wood</b></td>
</tr>

</table>

  </tr>
</table>

## Citation 

```
@inproceedings{garimella2023newborn,
  title={A Newborn Embodied Turing Test for Comparing Object Segmentation Across Animals and Machines},
  author={Garimella, Manju and Pak, Denizhan and Wood, Justin Newell and Wood, Samantha Marie Waters},
  booktitle={The Twelfth International Conference on Learning Representations},
  year={2023}
}
```

## Acknowledgements

We would like to acknowledge the members from our lab, [Lalit Pandey](https://github.com/L-Pandey), [Bhargav Desai](https://github.com/desaibhargav), for their work in providing checkpoints for the SimCLR model and building unity game to support agents with two-eyes respectively.

We would like to thank [RleXplore](https://github.com/RLE-Foundation/RLeXplore) for unsupervised algorithms (like ICM) and [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) for RL algorithm implementations.