#!/bin/bash

cd /home/ubuntu/DecisionTree64
read

if [[ -n "$TMUX" ]]; then
  echo "You are currently in a tmux session."
else
  echo "--- attach session ---"
  tmux attach-session -t ptb_main_astro
fi
read

# You are in the root ...
cd /home/ubuntu/DecisionTree64
read

echo "--- run env ---"
source venv310/bin/activate
read

echo "--- run ptb_main_astro ---"
python -m src.PTB_bot.ptb_main_astro

