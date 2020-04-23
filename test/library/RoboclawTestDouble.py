import serial
import subprocess
#import dronelauncher_python
from robot.api.deco import keyword
import psutil


class RoboclawTestDouble:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):

    @keyword
    def run(self):
        print("PASS")


if __name__ == "__main__":
    rc_test = RoboclawTestDouble()
    rc_test.run
