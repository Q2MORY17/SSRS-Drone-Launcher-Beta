#***Before using this example the motor/controller combination must be
#***tuned and the settings saved to the Roboclaw using IonMotion.
#***The Min and Max Positions must be at least 0 and 50000

import time
from roboclaw import Roboclaw

#Windows comport name
rc = Roboclaw("COM3",115200)
#Linux comport name
#rc = Roboclaw("/dev/ttyACM0",115200)

def displayspeed():
	enc1 = rc.ReadEncM1(address)
	speed1 = rc.ReadSpeedM1(address)

	print("Encoder1:"),
	if(enc1[0]==1):
		print enc1[1],
		print format(enc1[2],'02x'),
	else:
		print "failed",
	print "Speed1:",
	if(speed1[0]):
		print speed1[1]
	else:
		print "failed",
		
rc.Open()
address = 0x80

while(1):
        rc.ResetEncoders(address)
        rc.SpeedDistanceM1(address,500,2000,1)
        buffers = (0,0,0)
        while(buffers[1]!=0x80):	#Loop until distance command has completed
                displayspeed();
                buffers = rc.ReadBuffers(address);

        print "Primera llegada"
        time.sleep(2)

        rc.SpeedDistanceM1(address,-500,2000,1)
        buffers = (0,0,0)
        while(buffers[1]!=0x80):	#Loop until distance command has completed
                displayspeed();
                buffers = rc.ReadBuffers(address);

        print "Segunda llegada"	
        time.sleep(2)
