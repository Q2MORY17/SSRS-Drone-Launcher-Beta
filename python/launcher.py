"""
launcher.py creates the launcher object and its attributes
"""
from flask import Flask, render_template, request, jsonify
from roboclaw_3 import Roboclaw # This throws a warning but it works fine
import time
import socket
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('launcher.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class launcher(object):
    """
    launcher object is created - here, one roboclaw instance is created
    but one should be able to create as many roboclaw objects as one needs
    """

    #Open serial port
    #Linux comport name
    #rc = Roboclaw("/dev/ttyACM0",115200)
    #Windows comport name
    rc = Roboclaw("COM8",115200)
    rc.Open()
    encoders_ready = 0

    def __init__(self):
        pass

    class motor():
        """
        roboclaw configurations are added to the launcher object
        """

        def __init__(self, address, channel, pulses, length, speed_pulses, speed_manual, ready):
            self.address = address
            self.channel = channel
            self.pulses = pulses
            self.length = length
            self.speed_pulses = speed_pulses
            self.speed_manual = speed_manual
            self.ready = ready

    Master_M1 = motor(0x80, 1, 355000, 90.0, 7000, 127, 70.0)   # pitch
    Master_M2 = motor(0x80, 2, 950000, 180.0, 16000, 15, 10.0)  # rotation
    Slave_M1 = motor(0x81, 1, 19000, 130.0, 420, 127, 130.0)    # lift
    Slave_M2 = motor(0x81, 2, 14800, 111.0, 6*13400, 12, 0.0)   # launch has more variables...
    Slave_2_M1 = motor(0x82, 1, 5000, 0.0, 200, 127, 5.0)  # case left
    Slave_2_M2 = motor(0x82, 2, 5000, 0.0, 200, 127, 5.0)  # case right 

    """launch_acceleration=(launch_speed_pulses**2)/13400 #Acceleration during launch (pulses/second2)
    launch_max_speed=10           #Maximum launch speed
    launch_min_speed=1            #Minimum launch speed
    launch_max_acceleration=48    #Maximum launch acceleration
    launch_min_acceleration=1     #Minimum launch acceleration
    launch_standby=8000           #Drone position during stand-by
    launch_mount=17000            #Drone position during mounting
    launch_break=21000            #Belt position during breaking
    launch_bottom=0               #Drone position at the back part of the capsule
    launch_connect=2190           #Belt position for touching the upper part """

    def manual_up(self):
        """
        This should drive any motor controller:
            + UP for PITCH, COLUMN, CASE LEFT and CASE RIGHT
            + RIGHT for rotation motor
            + FORWARD for the launcher belt
        """
        try:
            if self.channel == 1:
                rc.ForwardM1(self.address, self.speed_manual)
                # return (''), 204 #Returns an empty response - Flask
            else:
                rc.ForwardM2(self.address, self.speed_manual)
                # return (''), 204 #Returns an empty response - Flask
        except:
            logger.info("I go up")
    
    def manual_down(self):
        """
        This should drive any motor controller:
            + DOWN for PITCH, COLUMN, CASE LEFT and CASE RIGHT
            + LEFT for rotation motor
            + BACKWARDS for the launcher belt
        """
        try:
            if self.channel == 1:
                rc.BackwardM1(self.address, self.speed_manual)
            # return (''), 204
            else:
                rc.BackwardM2(self.address, self.speed_manual)
        except:
            logger.info("I go down")
    
    def manual_position(self):
        """
        This should bring ANY motor, from their current position to a user defined position
        """
        try:
            """ if self.encoders_ready == 0: #Not execute if the encoders are not ready
                return (''), 403 """
            pitch_position = request.form.get('pitch_position', type=int)
            if pitch_position > self.pitch_length or pitch_position < 0:
                return (''), 400
            elif pitch_position == 0:
                pitch_objective = 0
            else:
                pitch_objective = int(self.pitch_pulses/(self.pitch_length/pitch_position))
            pitch_actual = rc.ReadEncM1(self.address)[1]
            pitch_increment = pitch_objective-pitch_actual
            if pitch_increment >= 0:
                rc.SpeedDistanceM1(self.address,self.pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
                return (''), 204
            else:
                rc.SpeedDistanceM1(self.address,-self.pitch_speed_pulses,-pitch_increment,1)
                rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
                return (''), 204
        except:
            logger.info("I go to a certain position")

    def prepare(self):
        pass

    def stop_all(self):
        pass

    def launch(self):
        pass

    def standby(self):
        pass
    
    def case_termometer(self):
        pass

    def CPU_temperature(self):
        pass

    def MPU92_65(self):
        pass

    def LED_strip(self):
        pass

SSRS_launcher = launcher()
SSRS_launcher.manual_up()
SSRS_launcher.manual_down()
SSRS_launcher.manual_position()
print(SSRS_launcher.Master_M1.address)
