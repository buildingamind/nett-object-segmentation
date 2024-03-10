# Analysis of Virtual Controlled Rearing Experiments
This repository generates standard graphs and measures one might like to see as a result of their simulations. 

Before using the code in this repo make sure that you have a run a simulation as described in the simulation folder. In order, to analyze the results please make sure you have R installed on the server as the analysis scripts are written in R.

## What to Analyze
The clearest data to be produced from a simulation is a performance graph. A performance graph is a bar plot of agents performance across all test trials for that agent. F

## Running an analysis
To run an analysis the user simply puts the run_id of their agent.
```
python run_analysis.py --log-dir ../../../data/runs/

```
python run.py --help
```
Once a graph is generated it will be located in the data/runs/ folder.
