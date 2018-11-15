import brickpi
import time
from Utility import Car
interface=brickpi.Interface()
interface.initialize()

Robot = Car(interface)
while True:
	goal_x = float(input("input your Wx:"))
	goal_y = float(input("input your Wy:"))
	Robot.navigateToWaypoint(goal_x, goal_y)
interface.terminate()
