"""
This code is being worked on @INFOTIV
AIM: Separate backend and frontend and make the code more readable.
CODER: Luan Mollakuqe
"""
# Libraries
from roboclaw_3 import Roboclaw # This throws a warning but it works fine
import time
import socket
from enum import Enum

class EncoderError(Exception):
    pass

# Classes with commands for manual pitch/lift/launch/rotation functions used in the launcher.
class PitchCMD(Enum):
    up = 1
    down = 2
    stop = 3

class LiftCMD(Enum):
    up = 1
    down = 2
    stop = 3

class LaunchCMD(Enum):
    up = 1
    down = 2
    stop = 3

class RotationCMD(Enum):
    right = 1
    left = 2
    stop = 3

class Launcher:
    def __init__(self):

        #setup variables

        #Linux comport name
        #self.rc = Roboclaw("/dev/ttyACM1",115200)

        #Windows com-port name
        self.rc = Roboclaw("COM8",115200)
        self.rc.Open()


        #Declare variables
        self.address = 0x80                #Controller 1, M1=Pitch, M2=Rotation
        self.address_2 = 0x81              #Controller 2, M1=Lift, M2=Launch

        self.pitch_pulses=355000           #Encoder pulses from the linear actuator
        self.pitch_length=90.0             #Degrees
        self.pitch_speed_pulses=7000       #Pulses per second
        self.pitch_speed_manual=75         #From 0 to 127
        self.pitch_ready=70.0              #Pitch degrees for the launch (temporary)

        self.rotation_pulses=950000        #Encoder pulses from the rotation motor
        self.rotation_length=180.0         #Degrees
        self.rotation_speed_pulses=16000   #Pulses per second
        self.rotation_speed_manual=127      #From 0 to 127
        self.rotation_ready=10.0           #Rotation degress for the launch (temporary)

        self.lift_pulses=19000             #Encoder pulses from the lifting colum
        self.lift_length=130.0             #cm
        self.lift_speed_pulses=420         #Pulses per second
        self.lift_speed_manual=127         #From 0 to 127 - 7 bits
        self.lift_ready=self.lift_length   #Lift lenght for the launch (temporary)

        self.launch_pulses=14800           #Encoder pulses from the launch motor
        self.launch_length=111.0           #cm
        self.launch_speed_pulses=6*13400   #Pulses per second during launch (145000 max) (13400 pulses/m)
        self.launch_speed_pulses_slow=2500 #Pulses per second during preparation
        self.launch_speed_manual=12        #From 0 to 127
        self.launch_acceleration=(self.launch_speed_pulses**2)/13400 #Acceleration during launch (pulses/second2)
        self.launch_max_speed=10           #Maximum launch speed
        self.launch_min_speed=1            #Minimum launch speed
        self.launch_max_acceleration=48    #Maximum launch acceleration
        self.launch_min_acceleration=1     #Minimum launch acceleration
        self.launch_standby=8000           #Drone position during stand-by
        self.launch_mount=17000            #Drone position during mounting
        self.launch_break=21000            #Belt position during breaking
        self.launch_bottom=0               #Drone position at the back part of the capsule
        self.launch_connect=2190           #Belt position for touching the upper part

        self.encoders_ready = 0            #At the beggining, the encoders are not ready

    def encoder_ready_check(self):
        '''
        Checks if encoder i ready.

        return:
            True or False
        '''
        if self.encoders_ready == 0:
            return False
        else:
            return True

# ---------------------------------------------------------------------------------
# ----------------- Pitch Functions -----------------------------------------------
# ---------------------------------------------------------------------------------

    def set_pitch_position(self, pitch_position):
        '''
        sets the pitch position of the launcher by the given pitch_position parameter.
        Args:
            pitch_position (float): desired pitch position for pitch motors in degrees

        '''
        if self.encoder_ready_check():
            # Checks conditions
            if pitch_position > self.pitch_length or pitch_position < 0:
                raise ValueError("out of bounds")
            elif pitch_position == 0:
                pitch_objective = 0
            else:
                pitch_objective = int(self.pitch_pulses / (self.pitch_length / pitch_position))

            pitch_increment = pitch_objective - self.rc.ReadEncM1(self.address)[1]

            if pitch_increment >= 0:
                self.rc.SpeedDistanceM1(self.address, self.pitch_speed_pulses,pitch_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM1(self.address, -self.pitch_speed_pulses, -pitch_increment, 1)
                self.rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
        else:
            raise EncoderError('Encoder Not Ready')

    def pitch_control(self, cmd: PitchCMD):
        '''
        Takes in a command (up, down or stop) and controlls the pitch accordingly
        Args:
            cmd (Pitch.CMD): desired movement command for  pitch motors (PitchCMD.up, PitchCMD.down, PitchCMD.stop)
        '''
        if  cmd == PitchCMD.up:
            self.rc.BackwardM1(self.address, self.pitch_speed_manual)
        if cmd == PitchCMD.down:
            self.rc.ForwardM1(self.address, self.pitch_speed_manual)
        if cmd == PitchCMD.stop:
            self.rc.ForwardM1(self.address, 0)

# ---------------------------------------------------------------------------------
# ------------------------ Rotation functions--------------------------------------
# ---------------------------------------------------------------------------------

    def set_rotation_position(self, rotation_position):
        '''
        sets the rotation position of the launcher by the given rotation_position parameter.
        Args:
            rotation_position (float): desired rotation position for rotation motors in degrees
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if rotation_position > self.lift_length or rotation_position < 0:
                raise ValueError("out of bounds")

            elif rotation_position == 0:
                rotation_objective = 0
            else:
                rotation_objective = int((self.rotation_pulses / (self.rotation_length / rotation_position))/2)
            rotation_increment = rotation_objective - self.rc.ReadEncM2(self.address)[1]
            if rotation_increment >= 0:
                self.rc.SpeedDistanceM2(self.address, self.rotation_speed_pulses,rotation_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM2(self.address,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM2(self.address, -self.rotation_speed_pulses, -rotation_increment, 1)
                self.rc.SpeedDistanceM2(self.address,0,0,0) #To avoid deceleration
        else:
            raise EncoderError('Encoder Not Ready')


    def rotation_control(self, cmd: RotationCMD):
        '''
        Takes in a command (right, left or stop) and controlls the rotation accordingly
        Args:
            cmd (Rotation.CMD): desired movement command for  lift motors (Rotation.right, Rotation.left, Rotation.stop)
        '''
        if cmd == RotationCMD.right:
            self.rc.ForwardM1(self.address_2, self.rotation_speed_manual)
            self.rc.ForwardM2(self.address_2, self.rotation_speed_manual)
        if cmd == RotationCMD.left:
            self.rc.BackwardM1(self.address_2, self.rotation_speed_manual)
            self.rc.BackwardM2(self.address_2, self.rotation_speed_manual)
        if cmd == RotationCMD.stop:
            self.rc.ForwardM1(self.address_2,0)
            self.rc.ForwardM2(self.address_2,0)

# ---------------------------------------------------------------------------------
# ------------------------ Lift functions--------------------------------------
# ---------------------------------------------------------------------------------
    def set_lift_position(self, lift_position):
        '''
        sets the lift position of the launcher by the given lift_position parameter.
        Args:
            lift_position (float): desired lift position on lift motors in centimeters
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if lift_position > self.lift_length or lift_position < 0:
                raise ValueError("out of bounds")
            elif lift_position == 0:
                lift_objective = 0
            else:
                lift_objective = int(self.lift_pulses / (self.lift_length / lift_position))

            lift_increment = lift_objective - self.rc.ReadEncM1(self.address_2)[1]

            if lift_increment >= 0:
                self.rc.SpeedDistanceM1(self.address_2, self.lift_speed_pulses,lift_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM1(self.address_2,0,0,0) #To avoid deceleration
                # set position cases
            else:
                self.rc.SpeedDistanceM1(self.address_2, -self.lift_speed_pulses, -lift_increment, 1)
                self.rc.SpeedDistanceM1(self.address_2,0,0,0) #To avoid deceleration
        else:
            raise EncoderError('Encoder Not Ready')

    def lift_control(self, cmd: LiftCMD):
        '''
        Takes in a command (up, down or stop) and controlls the lift accordingly
        Args:
            cmd (LiftCMD): desired movement command for  lift motors (LiftCMD.up, LiftCMD.down, LiftCMD.stop)
        '''
        if cmd == LiftCMD.up:
            self.rc.ForwardM1(self.address_2, self.lift_speed_manual)
        if cmd == LiftCMD.down:
            self.rc.BackwardM1(self.address_2, self.lift_speed_manual)
        if cmd == LiftCMD.stop:
            self.rc.ForwardM1(self.address_2, 0)

# ---------------------------------------------------------------------------------
# ------------------------ Launch functions--------------------------------------
# ---------------------------------------------------------------------------------

    def set_launch_position(self, launch_position):
        '''
        sets the launch position of the launcher by the given launch_position parameter.
        Args:
            launch_position (float): desired launch position in centimeters
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if launch_position > self.launch_length or launch_position < 0:
                raise ValueError("out of bounds")
            else:
                launch_objective = self.launch_bottom
                launch_increment = launch_objective - self.rc.ReadEncM2(self.address_2)[1]

            if launch_increment >= 0:
                self.rc.SpeedDistanceM2(self.address_2, self.launch_speed_pulses_slow, launch_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM2(self.address_2,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM2(self.address_2, -self.launch_speed_pulses_slow, -launch_increment, 1)
                self.rc.SpeedDistanceM2(self.address_2,0,0,0) #To avoid deceleration

            buffer_2 = (0,0,0)
            while(buffer_2[2]!=0x80):	#Loop until all movements are completed
                buffer_2 = self.rc.ReadBuffers(self.address_2)

            if launch_position == 0:
                launch_objective = 0
            else:
                launch_objective = int(self.launch_pulses / (self.launch_length / launch_position))

            launch_increment = launch_objective - self.rc.ReadEncM2(self.address_2)[1] + self.launch_connect
            if launch_increment >= 0:
                self.rc.SpeedDistanceM2(self.address_2, self.launch_speed_pulses_slow, launch_increment, 0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM2(self.address_2, 0, 0, 0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM2(self.address_2, -self.launch_speed_pulses_slow, -launch_increment,0)
                self.rc.SpeedDistanceM2(self.address_2, 0, 0, 0) #To avoid deceleration
        else:
            raise EncoderError('Encoder Not Ready')


    def launch_control(self, cmd: LaunchCMD):
        '''
        Takes in a command (forwards, backwards or stop) and controlls the launch accordingly
        Args:
            cmd (LaunchCMD): desired launch movement for launch motors, (for example: Launch.CMD.forwards)
        '''
        if cmd == LaunchCMD.up:
            self.rc.ForwardM2(self.address_2, self.launch_speed_manual)
        if cmd == LaunchCMD.down:
            self.rc.BackwardM2(self.address_2, self.launch_speed_manual)
        if cmd == LaunchCMD.stop:
            self.rc.ForwardM2(self.address_2, 0)

    def stop(self):
        '''
        stops all motors
        '''
        self.rc.ForwardM1(self.address, 0)
        self.rc.ForwardM2(self.address, 0)
        self.rc.ForwardM1(self.address_2, 0)
        self.rc.ForwardM2(self.address_2, 0)

    def max_pitch(self):

        if self.encoder_ready_check():
            pitch_increment = self.pitch_pulses - self.rc.ReadEncM1(self.address)[1]
            if pitch_increment >= 0:
                self.rc.SpeedDistanceM1(self.address,self.pitch_speed_pulses,pitch_increment,1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM1(self.address,-self.pitch_speed_pulses,-pitch_increment,1)
                self.rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration

    def min_pitch(self):
        pass

    def min_lift(self):
        pass

    def max_lift(self):
        pass



    def home(self):
        pass

    def reset_encoders(self):
        #TODO: reset encoder. Either set to "1" (ready) OR make the inverse of what it is now.

        #example 1:
        self.encoders_ready = 1

        #example 2:

        pass

    def battery_voltage(self):
        '''
        Calculates and returns battery voltage

        param:
            none
        return:
            voltage (float): represents battery voltage
        '''
        voltage = round(0.1 * self.rc.ReadMainBatteryVoltage(self.address)[1],2)
        return voltage


# ---------------------------------------------------------------------------------
# ------------------------ Automated functions--------------------------------------
# ---------------------------------------------------------------------------------
    def standby(self):
        '''
        Sets pitch, rotation, lift and launch to zero, which is the home position.

        '''
        self.set_pitch_position(0)
        self.set_rotation_position(0)
        self.set_lift_position(0)
        self.set_launch_position(0)

    def set_launch_variables(self, pitch_position, rotation_position, lift_position):
        '''
        Sets the variables before preparing the launch.

            Args:
        pitch_position      (int): desired pitch position between values x and y
        rotation_position   (int): desired rotation position between x and y
        lift_position       (int): desired lift position in between values x and y
        launch_position     (int): desired launch position in between values x and y
        '''
        self.change_pitch(pitch_position)       #Updates self.pitch_ready
        self.change_rotation(rotation_position) #Updates self.rotation_ready
        self.change_lift(lift_position)         #Updates self.lift_ready

    def prepare_launch(self):
        '''
        Configures the launchers pitch, rotation and lift according to the variables set in set_launch_variables().
        also sets launch position to zero, since that is the start position before launch

        '''
        self.set_pitch_position(self.pitch_ready)
        self.set_rotation_position(self.rotation_ready)
        # Changed self.lift_position to self.lift_ready since there is no variable named lift_position
        self.set_lift_position(self.lift_ready)
        self.set_launch_position(0)

    def launch(self):
        '''
        launch operates the launch motor  + belt.
        when this runs, the drone launches into the air.

        '''
        pass

    def mount(self):
        pass

    def automatic_launch(self):
        pass

# ---------------------------------------------------------------------------------
# ------------------------ Variable update functions-------------------------------
# ---------------------------------------------------------------------------------

    def change_pitch(self, pitch_position):
        if pitch_position > self.pitch_length or pitch_position < 0:
            raise ValueError("Out of Bounds")
        else:
            self.pitch_ready = pitch_position


    def change_lift(self, lift_position):
        if lift_position > self.lift_length or lift_position < 0:
            raise ValueError("Out of Bounds")
        else:
            self.lift_ready = lift_position

    def change_rotation(self, rotation_position):
        if rotation_position > self.rotation_length or rotation_position < 0:
            raise ValueError("Out of Bounds")
        else:
            self.rotation_ready = rotation_position

    def change_speed(self, speed):
        if speed > self.launch_max_speed or speed < self.launch_min_speed:
            raise ValueError("Out of Bounds")
        else:
            if speed > 7:
                self.launch_speed_pulses = speed*13400
                self.launch_acceleration = 655360 #maximum value
            else:
                self.launch_speed_pulses = speed*13400
                self.launch_acceleration = (self.launch_speed_pulses**2)/13400


    def change_acceleration(self, acceleration):
        if acceleration > self.launch_max_acceleration or acceleration < self.launch_min_acceleration:
            raise ValueError("Out of Bounds")
        else:
            self.launch_acceleration = acceleration*13400

    def disable_buttons(self):
        pass



launch = Launcher()
