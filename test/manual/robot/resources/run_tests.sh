#!/bin/bash
#DRONE_IP=$(hostname -i | cut -f2 -d " ")
IP=$(python ./library/getip.py)
PORT=5000
URL="http://$IP:$PORT"
BROWSER="chrome"
OPTS="-v URL:$URL -v BROWSER:$BROWSER -d results"
echo $DRONE_IP > .current_ip

python ../../../python/dronelauncher_python.py &> /dev/null &
DRONE_PID=$!

if [ $# -eq 0 ]; then           #If argumentlist is empty, run all tests.
    for i in *.robot
    do
	robot $OPTS $i
    done
else                            # Run tests provided by argument.
    for i in $@
    do
	robot $OPTS $i
    done
fi

kill $DRONE_PID

if [ -f .current_ip ]; then
    rm .current_ip
fi

exit 0
