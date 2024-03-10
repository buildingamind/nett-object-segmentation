#!/bin/bash
python src/simulation/run.py ++run_id='parsing_ego4d_lstm_fork_A_nf_exp1' ++Environment.use_ship=False ++Environment.background=A ++Agent.policy=LSTM
python src/simulation/run.py ++run_id='parsing_ego4d_lstm_fork_A_nf_exp2' ++Environment.use_ship=False ++Environment.background=A ++Agent.policy=LSTM
