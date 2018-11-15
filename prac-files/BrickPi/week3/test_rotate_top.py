import threading
import time
import sys
from BrickPi.Utility import Car
import BrickPi

interface=brickpi.Interface()
interface.initialize()
interface.startLogging("motor_position_1.log")

Robot = Car(interface, config_file='carpet_params.json')


# Robot.rotate_ultrasonic_motor(float(sys.argv[1]))
Robot.set_ultra_pose(float(sys.argv[1]))

interface.stopLogging()
interface.terminate()