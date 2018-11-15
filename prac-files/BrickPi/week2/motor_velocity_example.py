import brickpi
import time
from BrickPi.Utility import Car
interface=brickpi.Interface()
interface.initialize()

Robot = Car(interface)

Robot.moveForward(6)

print "Press Ctrl+C to exit"
while True:
	time.sleep(1)

interface.terminate()
