# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:42:47 2020

@author: kent1
"""
from flask import Flask, render_template, request, jsonify
from roboclaw_3 import Roboclaw # This throws a warning but it works fine
import time
import socket
import logging

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
#
#formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
#
#file_handler = logging.FileHandler('launcher.log')
#file_handler.setLevel(logging.INFO)
#file_handler.setFormatter(formatter)
#
#logger.addHandler(file_handler)

logging.basicConfig(filename='launcher.log',level=logging.DEBUG)

#Open serial port
#Linux comport name
#rc = Roboclaw("/dev/ttyACM0",115200)
#Windows comport name
rc = Roboclaw("COM8",115200)
rc.Open()
encoders_ready = 1 # set to 1 so that the position method can be tested

origo = [90.0, 0, 0, 0]
actual_coordonates = origo[:]
case_open = 0 

class motor():

    def __init__(self, address, channel, pulses, length, speed_pulses, speed_manual, ready):
        self.address = address
        self.channel = channel
        self.pulses = pulses
        self.length = length
        self.speed_pulses = speed_pulses
        self.speed_manual = speed_manual
        self.ready = ready
    
    def up(self):
        command = [rc.ForwardM1, rc.ForwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(f"{command[self.channel]}")
    
    def down(self):
        command = [rc.BackwardM1, rc.BackwardM2]
        try:
            command[self.channel](self.address, self.speed_manual)
        except AttributeError:
            print(f"{command[self.channel]}")

    def position(self):
        """
        This method is still bound to pitch in a way but it is good for testing
        """
        command = [rc.SpeedDistanceM1, rc.SpeedDistanceM2, rc.ReadEncM1, rc.ReadEncM2]
        if encoders_ready == 0: #Not execute if the encoders are not ready
            return (''), 403 
        try:
            position = request.form.get('pitch_position', type=int)
        except RuntimeError:
            position = int(input('which position do you want to reach: '))
        if position > self.length or position < 0:
            return ('Out of bounds'), 400
        elif position == 0:
            objective = 0
        else:
            objective = int(self.pulses/(self.length/position))
            print(f'objective = {objective}')
        try:
            actual = command[self.channel+2](self.address)[1]
        except AttributeError:
            actual = 0 # Set this to any value between 0 and self.pulses
            print(f'starting point: {actual/(self.pulses/self.length)} degrees')
        increment = objective-actual
        if increment >= 0:
            try:
                command[self.channel](self.address,self.speed_pulses,increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                command[self.channel](self.address,0,0,0) #To avoid deceleration
            except AttributeError:
                print(f'I go {increment} steps')
                print(f'{self.address}, {self.speed_pulses}, {increment}')
#                logger.info(f'{command[self.channel]}')
        else:
            try:
                command[self.channel](self.address,-self.speed_pulses,-increment,1)
                command[self.channel](self.address,0,0,0) #To avoid deceleration
            except AttributeError:
                print(f'I go {increment} steps')
                print(f'{self.address}, {self.speed_pulses}, {increment}')
#                logger.info(f'{command[self.channel]}')
                
    def stop(self):
        command = [rc.ForwardM1, rc.ForwardM2]
        try:
            command[self.channel](self.address, 0)
        except AttributeError:
            print(f"{command[self.channel]}")
    
pitch = motor(0x80, 0, 355000, 90.0, 7000, 127, 70.0)   # pitch
rotation = motor(0x80, 1, 950000, 180.0, 16000, 15, 10.0)  # rotation
lift = motor(0x81, 0, 19000, 130.0, 420, 127, 130.0)    # lift
launch = motor(0x81, 1, 14800, 111.0, 6*13400, 12, 0.0)   # launch has more variables...
caseL = motor(0x82, 0, 5000, 5.0, 200, 127, 5.0)  # case left
caseR = motor(0x82, 1, 5000, 5.0, 200, 127, 5.0)  # case right 

pitch.up()
#Master_M1.down()
#Slave_M2.position()
print(pitch.address, lift.address, caseL.address)

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
