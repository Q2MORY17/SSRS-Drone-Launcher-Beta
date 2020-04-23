import serial
import subprocess


class RoboclawTestDouble:
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
    rc_test.run
