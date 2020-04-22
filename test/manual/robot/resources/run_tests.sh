#!/bin/bash
#DRONE_IP=$(hostname -i | cut -f2 -d " ")
DRONE_IP=$(python ./library/getip.py)

python ../../../python/dronelauncher_python.py &> /dev/null &
DRONE_PID=$!


# if [ $# -eq 0 ]; then
#     robot -d results *.robot
# else
#     robot -d results $@
# fi

echo $DRONE_IP
echo $DRONE_PID
kill $DRONE_PID

exit 0

