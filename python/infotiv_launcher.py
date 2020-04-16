"""
This code is being worked on @INFOTIV
AIM: Separate backend and frontend and make the code more readable. 
CODER: Luan
"""
# Libraries
from roboclaw_3 import Roboclaw # This throws a warning but it works fine
import time
import socket
from enum import Enum

    # TODO: merge functions like "pitch_up, down, position and stop" into one function, which takes a parameter instead


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
        #Open serial port
        #Linux comport name
        self.rc = Roboclaw("/dev/ttyACM0",115200)
        #Windows comport name
        #self.rc = Roboclaw("COM8",115200)
        self.rc.Open()

        #Look for the appropriate local network. based on the Raspberry Pi IP address - RPi Terminal -> Hostname -I or ifconfig
        self.host=(([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
        port=5000

        #Declare variables
        self.address = 0x80                #Controller 1, M1=Pitch, M2=Rotation
        self.address_2 = 0x81              #Controller 2, M1=Lift, M2=Launch

        self.pitch_pulses=355000           #Encoder pulses from the linear actuator
        self.pitch_length=90.0             #Degrees
        self.pitch_speed_pulses=7000       #Pulses per second
        self.pitch_speed_manual=75        #From 0 to 127
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
        self.lift_ready=self.lift_length        #Lift lenght for the launch (temporary)

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
        #Check if encoder is ready
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
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if pitch_position > self.lift_length or pitch_position < 0:
                #TODO: return error
                pass
            elif pitch_position == 0:
                pitch_objective = 0
            else:
                pitch_objective = int(self.pitch_pulses / (self.pitch_length / self.pitch_position))
                
            pitch_increment = pitch_objective - self.rc.ReadEncM1(self.address)[1]

            if pitch_increment >= 0:
                self.rc.SpeedDistanceM1(self.address, self.pitch_speed_pulses,pitch_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                rc.SpeedDistanceM1(address,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM1(self.address, -self.pitch_speed_pulses, -pitch_increment, 1)
                rc.SpeedDistanceM1(self.address,0,0,0) #To avoid deceleration
        else:
            #return Error?
            pass

    def pitch_control(self, cmd):
        '''
        Takes in a command (up, down or stop) and controlls the pitch accordingly
        '''
        if  cmd == 'up':
            self.rc.BackwardM1(self.address, self.pitch_speed_manual)
        if cmd == PitchCMD.down:
            self.rc.ForwardM1(self.address, self.pitch_speed_manual)
        if cmd == 'stop':
            self.rc.ForwardM1(self.address, 0)

# ---------------------------------------------------------------------------------
# ------------------------ Rotation functions--------------------------------------
# ---------------------------------------------------------------------------------

    def set_rotation_position(self, rotation_position):
        '''
        sets the rotation position of the launcher by the given rotation_position parameter.
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if rotation_position > self.lift_length or rotation_position < 0:
                #TODO: return error
                pass
            elif rotation_position == 0:
                rotation_objective = 0
            else:
                rotation_objective = int((self.rotation_pulses / (self.rotation_length / self.rotation_position))/2)
                
            rotation_increment = rotation_objective - self.rc.ReadEncM2(self.address)[1]

            if rotation_increment >= 0:
                self.rc.SpeedDistanceM2(self.address, self.rotation_speed_pulses,rotation_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM2(self.address,0,0,0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM2(self.address, -self.rotation_speed_pulses, -rotation_increment, 1)
                rc.SpeedDistanceM2(self.address,0,0,0) #To avoid deceleration
        else:
            #return Error?
            pass


    def rotation_control(self, cmd):
        '''
        Takes in a command (right, left or stop) and controlls the rotation accordingly
        '''
        if cmd == 'right':
            self.rc.ForwardM1(self.address_2, self.rotation_speed_manual)
        if cmd == 'left':
            self.rc.BackwardM1(self.address_2, self.rotation_speed_manual)
        if cmd == 'stop':
            self.rc.ForwardM1(self.address_2,0)

# ---------------------------------------------------------------------------------
# ------------------------ Lift functions--------------------------------------
# ---------------------------------------------------------------------------------
    def set_lift_position(self, lift_position):
        '''
        sets the lift position of the launcher by the given lift_position parameter.
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if lift_position > self.lift_length or lift_position < 0:
                #TODO: return error
                pass
            elif lift_position == 0:
                lift_objective = 0
            else:
                lift_objective = int(self.lift_pulses / (self.lift_length / self.lift_position))
                
            lift_increment = lift_objective - self.rc.ReadEncM1(self.address_2)[1]

            if lift_increment >= 0:
                self.rc.SpeedDistanceM1(self.address_2, self.lift_speed_pulses,lift_increment, 1) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM1(self.address_2,0,0,0) #To avoid deceleration
                # set position cases
            else:
                self.rc.SpeedDistanceM1(self.address_2, -self.lift_speed_pulses, -lift_increment, 1)
                rc.SpeedDistanceM1(self.address_2,0,0,0) #To avoid deceleration
        else:
            #return Error?
            pass

    def lift_control(self, cmd: LiftCMD):
        '''
        Takes in a command (up, down or stop) and controlls the lift accordingly
        '''
        if cmd == LiftCMD.up:
            self.rc.ForwardM1(self.address_2, self.lift_speed_manual)
        if cmd == LiftCMD.down:
            self.rc.BackwardM1(self.address_2, self.lift_speed_manual)
        if cmd == LiftCMD.position:
            self.set_lift_position()
        if cmd == LiftCMD.stop:
            self.rc.ForwardM1(self.address_2, 0)


# ---------------------------------------------------------------------------------
# ------------------------ Launch functions--------------------------------------
# ---------------------------------------------------------------------------------
    
    def set_launch_position(self, launch_position):
        '''
        sets the launch position of the launcher by the given launch_position parameter.
        '''
        if self.encoder_ready_check():
            # Checks conditions
            if launch_position > self.launch_length or launch_position < 0:
                #TODO: return error
                pass
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
                launch_objective = int(self.launch_pulses/(self.launch_length/self.launch_position))

            launch_increment = launch_objective - self.rc.ReadEncM2(self.address_2)[1] + self.launch_connect
            if launch_increment >= 0:
                self.rc.SpeedDistanceM2(self.address_2, self.launch_speed_pulses_slow, launch_increment, 0) #(address, +-speed, pulses, buffer(0=buffered, 1=Execute immediately))
                self.rc.SpeedDistanceM2(self.address_2, 0, 0, 0) #To avoid deceleration
            else:
                self.rc.SpeedDistanceM2(self.address_2, -self.launch_speed_pulses_slow, -launch_increment,0)
                self.rc.SpeedDistanceM2(self.address_2, 0, 0, 0) #To avoid deceleration
        else:
            #return error?
            pass


    def launch_control(self, cmd: LaunchCMD):
        '''
        Takes in a command (forwards, backwards or stop) and controlls the launch accordingly
        '''
        if cmd == LaunchCMD.forwards:
            self.rc.ForwardM2(self.address_2, self.launch_speed_manual)
        if cmd == LaunchCMD.backwards:
            self.rc.BackwardM2(self.address_2, self.launch_speed_manual)
        if cmd == LaunchCMD.stop:
            self.rc.ForwardM2(self.address_2,0)



    def max_pitch(self):
        
        if self.encoder_ready_check():
            pitch_increment = self.pitch_pulses - self.rc.ReadEncM1(address)[1]
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
        pass

    def battery_voltage(self):
        pass

    def stop(self):
        pass


    # AUTOMATED FUNCTIONS:

    def standby(self):
        pass

    def prepare(self):
        pass

    def launch(self):
        pass

    def mount(self):
        pass

    def automatic_laumch(self):
        pass

    # variable update

    def change_pitch(self):
        pass

    def change_lift(self):
        pass

    def change_rotation(self):
        pass

    def change_speed(self):
        pass

    def change_acceleration(self):
        pass

    def disable_buttons(self):
        pass



launch = Launcher()


