#!/bin/bash

echo "--- create sessions ---"
tmux new -d -s ptb_main_astro
#tmux detach
tmux new -d -s ptb_main_recorder
tmux new -d -s ptb_binance_monitor

echo "--- check sessions ---"
tmux list-sessions


# You are in the root ...
cd /home/ubuntu/DecisionTree64

echo "--- update DecisionTree64 repo ---"
git reset --hard origin/develop
git fetch
git switch develop
git pull origin develop


# You are in the root ...
cd /home/ubuntu/BinanceTrader

echo "--- update BinanceTrader repo ---"
git reset --hard origin/develop
git fetch
git switch develop
git pull origin develop


cd /home/ubuntu

echo "--- make scripts executable ---"
chmod +x ./DecisionTree64/ptb_main_astro.sh
chmod +x ./DecisionTree64/ptb_main_recorder.sh
chmod +x ./BinanceTrader/ptb_binance_monitor.sh
