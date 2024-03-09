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
├── docs                             # Documentation and guides
├── data												                 # Placeholder to storing executables, runs and checkpoints
│   ├── checkpoints 
│   │   └── simclr
│   ├── executables
│   │   ├── parsing_benchmark2eyed
│   │   └── parsing_benchmark
│   └── runs
├── LICENSE											               # License file
├── README.md													           # Readme file
├── requirements.txt									        # requirements.txt file containing project requirements
├── scripts														            # Example scripts for running experiments
│   └── parsing_sup.sh
├── setup.cfg
├── src															               # Folder containing src code
│   ├── analysis											          # Folder containing R-scripts for doing analysis
│   │   ├── r														
│   │   └── README.md
│   └── simulation										         # Folder containing simulation code for experiments
│       ├── agent											         # Agent configuration
│       ├── algorithms								       # Algorithms - like Intrinsic curiosity module
│       ├── callback									        # Callback functions to compute metrics during training
│       ├── common											        # Common function
│       ├── conf										           # Hydra configuration for running experiments
│       ├── env_wrapper								      # Environment wrapper 
│       ├── GPUtil.py										      # GPUUtils functions
│       ├── networks										       # Encoders models
│       ├── run.py                   # Main file to run experiment
│       └── utils.py										       # Utility functions
└── tests															             # pytests folder
    ├── pytest.ini		
    └── test_env.py

```
## Getting Started

The section describes how to get started with running the experiments and performing the analysis of the results.

### Installation

## How to Install

In this section, you will pull this repository from Github, open the Unity environment, and build the ChickAI environment as an executable.

### Codebase Installation

1. **Install Git and/or Github Desktop ** : If you install Git, you'll be able to interact with Github through the command line. You can download Git using the directions here: [https://git-scm.com/downloads](https://git-scm.com/downloads). If you install Git Desktop, you can use a GUI to interact with Github. You can install Github Desktop by following the directions here: [https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/](https://docs.github.com/en/desktop/installing-and-configuring-github-desktop/). For the following steps, I will provide the command line arguments (but you can use the GUI to find the same options in Github Desktop).

2. To download the repository, click the Code button on the nett-object-segmentation repo. Copy the provided web URL. Then follow the code below to change to directory where you want the repo (denoted here as MY_FOLDER) and then clone the repo.
   ```
   cd MY_FOLDER
   git clone URL_YOU_COPIED_GOES_HERE
   ```
   
3. **Virtual Environment Setup** (Highly Recommended): Create and activate a virtual environment to avoid dependency conflicts.
   ```bash
   conda create -y -n nett_env python=3.8.17
   conda activate nett_env
   ```
   See [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda "Link for how to set-up a virtual env") for detailed instructions.

5. Install the needed versions of `setuptools` and `pip`:
   ```bash
   pip install setuptools==65.5.0 pip==21 wheel==0.38.4
   ```
   **NOTE:** This is a result of incompatibilities with the subdependency `gym==0.21`. More information about this issue can be found [here](https://github.com/openai/gym/issues/3176#issuecomment-1560026649)

3. **Installation for other dependency**: Install the dependency using `pip`.
   ```bash
   pip install -r requirements.txt
   ```

### Running an Experiment (default configuration)

After having followed steps 1-5 above once experiments can be run with a few lines of code

```
  bash scripts/parsing_sup.sh
```

### Running Standard Analysis

After running the experiments, the pipeline will generate a collection of datafiles in the `Data` folder. To run the analyses performed in the papers you can use the following command

```
python3 src/analysis/r/run_analysis.py
```

This will generate a collection of graphs in the folder `data/runs`.

### Running an Experiment (custom configuration)

After having replicated the results with the default configuration, you may wish to experiment by plugging in different brains for the agent. We have included a few different possible brains for the agent. To plug these in simply modify the `yaml` file in `src/simulation/conf/Agent/basic.yaml`.

```
encoder: BRAIN
```

where **BRAIN** can be set to [small, medium, or large] which correspond to a 4-layer CNN, 10-Layer ResNet, and 18-layer ResNet respectively.

Note that if you change the size of the encoder, you may also consider changing the number of training episodes. This can be done in the config file `src/simulation/conf/config.yaml`.

```
train_eps: NEW_EPISODE_COUNT
```

If you wish to experiment with custom architectures or a new policy network, this can be done by modifying the agent script (`Simulation/agent.py`**). **`self.model` is the policy network and `self.encoder` is the encoder network. Both can be assigned any appropriately sized **`torch.nn.module`**.


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
