import brickpi
from BrickPi.Utility import Car

interface=brickpi.Interface()
interface.initialize()
Robot = Car(interface)
for i in range(4):
    Robot.moveForward(40)
    Robot.moveLeft(90)
interface.terminate()

