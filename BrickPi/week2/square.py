import brickpi
from BrickPi.Utility import Car

interface=brickpi.Interface()
interface.initialize()
Robot = Car(interface,config_file='carpet_params.json')
for i in range(4):
    Robot.moveForward(40)
    Robot.moveLeft(90)
interface.terminate()

