import serial
import subprocess
#import dronelauncher_python
from robot.api.deco import keyword
import psutil


class RoboclawTestDouble:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    com_port_app = "setupg.exe"
    com_port_app_path = "C:\\Program Files (x86)\\com0com\\"

    def __init__(self):
        if self.com_port_app in (p.name() for p in psutil.process_iter()):
            if not subprocess.Popen(self.com_port_app_path + self.com_port_app, shell=True):
                raise FileNotFoundError(self.com_port_app_path)

    @keyword
    def run(self):
        print("PASS")


if __name__ == "__main__":
    rc_test = RoboclawTestDouble()
    rc_test.run
