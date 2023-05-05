#!/bin/bash

echo "--- make scripts executable ---"
chmod +x ./DecisionTree64/ptb_main_astro.sh
chmod +x ./DecisionTree64/ptb_main_recorder.sh
chmod +x ./BinanceTrader/ptb_binance_monitor.sh

echo "--- open session ---"
tmux new -d -s ptb_main_astro
#tmux detach
tmux new -d -s ptb_main_recorder
#tmux detach
tmux new -d -s ptb_binance_monitor
#tmux detach
#tmux a -t ptb_binance_monitor

echo "--- check sessions ---"
tmux list-sessions




