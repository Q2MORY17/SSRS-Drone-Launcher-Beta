#!/bin/bash
#DRONE_IP=$(hostname -i | cut -f2 -d " ")
DRONE_IP=$(python ./library/getip.py)
echo $DRONE_IP > .current_ip

python ../../../python/dronelauncher_python.py &> /dev/null &
DRONE_PID=$!

if [ $# -eq 0 ]; then           #If argumentlist is empty, run all tests.
    for i in *.robot
    do
	robot -d results $i
    done
else                            # Run tests provided by argument.
    for i in $@
    do
	robot -d results $i
    done
fi

kill $DRONE_PID

if [ -f .current_ip ]; then
    rm .current_ip
fi

exit 0
