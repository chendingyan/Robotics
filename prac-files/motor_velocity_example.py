import brickpi
import time
from Utility import Car
interface=brickpi.Interface()
interface.initialize()

Robot = Car(interface)

#Robot.moveDistance(10)
# Robot.left90()
Robot.rotate(90)
# print "Press Ctrl+C to exit"
# while True:
#     time.sleep(1)

interface.terminate()
