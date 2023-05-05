#!/bin/bash

echo "--- attach session ---"
tmux attach-session -t ptb_main_astro

# You are in the root ...
cd /home/ubuntu/DecisionTree/

#echo "--- update repo ---"
#git fetch
#git switch develop
#git pull origin develop

echo "--- run env ---"
source venv310/bin/activate

echo "--- run python script ---"
python -m src.PTB_bot.ptb_main_astro

