#!/bin/bash

IP=$(python3 ./library/getip.py)
PORT=5000
URL="http://$IP:$PORT"
BROWSER="chrome"
OPTS="-v URL:$URL -v BROWSER:$BROWSER -d results"
LOG=.dronelauncher.log

#
# Check if firefox exists on windows based systems
#

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    if [ -d "/c/Program Files/Mozilla Firefox" ]; then
	export PATH="$PATH:/c/Program Files/Mozilla Firefox"
    elif [ -d "/d/Program Files/Mozilla Firefox" ]; then
	export PATH="$PATH:/d/Program Files/Mozilla Firefox"
    else
	echo -e "\nFirefox not found in usual places, please add to path!\n"
    fi
fi


python3 ../../../python/dronelauncher_python.py &> $LOG &
DRONE_PID=$!

if [ $# -eq 0 ]; then           #If argumentlist is empty, run all tests.
    for i in *.robot
    do
	robot $OPTS $i
    done
    
    if [ -x "$(command -v firefox)" ]; then
	BROWSER="firefox"
	OPTS="-v URL:$URL -v BROWSER:$BROWSER -d results"
	
	for i in *.robot             
	do
	    robot $OPTS $i
	done
    fi

else                            # Run tests provided by arguments.
    for i in $@
    do
	robot $OPTS $i
    done

    # Check if firefox installed on unixbased systems
    if [ -x "$(command -v firefox)" ]; then
	BROWSER="firefox"
	OPTS="-v URL:$URL -v BROWSER:$BROWSER -d results"
	for i in $@
	do
	    robot $OPTS $i
	done
    else
	echo -e "\nFirefox not installed! skipping firefox tests...\n"
    fi
fi

if [ -f $LOG ]; then
    rm $LOG
fi

kill $DRONE_PID

exit 0
