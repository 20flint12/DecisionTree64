#!/bin/bash

echo "--- attach session ---"
tmux attach-session -t ptb_main_recorder

# You are in the root ...
cd /home/ubuntu/DecisionTree/

echo "--- run env ---"
source venv310/bin/activate

echo "--- run ptb_main_recorder ---"
python -m src.PTB_bot.ptb_main_recorder

