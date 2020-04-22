#!/bin/bash
DRONE_IP=$(hostname -i | cut -f2 -d " ")

python ../../../python/dronelauncher_python.py &> ./logs/dronelauncher.log &
DRONE_PID=$!

if [ $# -eq 0 ]; then
    robot -d results *.robot
else
    robot -d results $@
fi

kill $DRONE_PID

exit 0

