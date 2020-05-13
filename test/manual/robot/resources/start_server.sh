#!/bin/bash
python ../../../python/dronelauncher_python.py &> >(sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g") &> .dronelauncher.log
exit 0
