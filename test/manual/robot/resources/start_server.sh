#!/bin/bash
python ../../../python/dronelauncher_python.py >> logs/dronelauncher.log
DRONE_PID=$!
DRONE_IP=hostname -i | cut -f2 -d " "
