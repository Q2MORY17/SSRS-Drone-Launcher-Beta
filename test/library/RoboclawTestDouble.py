import serial
import subprocess


class RoboclawTestDouble:
    """
    Class to be used as a Library in RobotFramework.
    To read the commands sent to the roboclaw, a virtual COM port pair shall be setup using
    com0com, https://sourceforge.net/projects/com0com/files/latest/download (install with defaults)
    Start the com0com application and setup the port names to be port names used in
    dronelauncher_python.py (COM8) and the one used here (COM5)

    The com0com application need to be started manually before running the tests.
    """

    # Uses GLOBAL scope to not open the port for each test case
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    com_port = "COM5"

    def __init__(self):
        try:
            self.virtual_com_port = serial.Serial(self.com_port, timeout=0.5)
        except:
            raise SystemError("Could not connect to " + self.com_port)

    def read_roboclaw_command(self):
        command = self.virtual_com_port.readline()

        if not command:
            raise AssertionError("No command was sent to the roboclaw")

        print(command)
        return


if __name__ == "__main__":
    rc_test = RoboclawTestDouble()
    rc_test.read_roboclaw_command()
