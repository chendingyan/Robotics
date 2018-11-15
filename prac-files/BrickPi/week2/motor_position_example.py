import brickpi
import time
import math
from BrickPi.Utility import Car

def fun(mode):

    return

interface=brickpi.Interface()
interface.initialize()
Robot = Car(interface)
mode = int(input("Which parameter you want to tune?\nType 1 for Kp, 2 for Ki, 3 for Kd"))
min = int(input("Enter minimum:"))
max = int(input("ENter maximum:"))
increment = int(input("Enter incremental value:"))
dict = {'min':min, 'max': max, 'increment': increment, 'mode':mode}


input_angle = float(input("Enter a angle to rotate (in degree): "))

with open("logs/logs_name.txt", "w") as f:
    for i in range(min, max, increment, input_angle):
        if dict['mode'] == 1:
            Robot.motorParams["Left"].pidParameters.k_p = i
            Robot.motorParams["Right"].pidParameters.k_p = i
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[0], Robot.motorParams["Left"])
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[1], Robot.motorParams["Right"])
            name = "motor_angle_" + str(input_angle) + "Kp_value_" + str(i)
        elif dict['mode'] == 2:
            Robot.motorParams["Left"].pidParameters.k_i = i
            Robot.motorParams["Right"].pidParameters.k_i = i
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[0], Robot.motorParams["Left"])
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[1], Robot.motorParams["Right"])
            name = "motor_angle_" + str(input_angle) + "Ki_value_" + str(i)
        elif dict['mode'] == 3:
            Robot.motorParams["Left"].pidParameters.k_d = i
            Robot.motorParams["Right"].pidParameters.k_d = i
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[0], Robot.motorParams["Left"])
            Robot.interface.setMotorAngleControllerParameters(Robot.motors[1], Robot.motorParams["Right"])
            name = "motor_angle_" + str(input_angle) + "Kd_value_" + str(i)
        f.write(name+'\n')
        angle = math.radians(input_angle)
        Robot.wheel_rotate(angle, name)
        time.sleep(0.5)


interface.terminate()

