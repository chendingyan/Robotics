import brickpi
import time
import json
import math
class Car:
    def __init__(self, interface, touch_port, sonar_port):
        # touch_port and sonar_port
        self.interface = interface
        self.motors = [0,2]
        self.motorParams = {}
        self.interface.motorEnable(self.motors[0])
        self.interface.motorEnable(self.motors[1])
        self.touch_port = None
        self.sonar_port = None
        # Import parameters
        with open("parameter.json", "r") as f:
            params = json.load(f)

        self.motorParams["Left"] = self.interface.MotorAngleControllerParameters()
        self.motorParams["Left"].maxRotationAcceleration = params["Left"]["maxRotationAcceleration"]
        self.motorParams["Left"].maxRotationSpeed = params["Left"]["maxRotationSpeed"]
        self.motorParams["Left"].feedForwardGain = params["Left"]["feedForwardGain"]
        self.motorParams["Left"].minPWM = params["Left"]["minPWM"]
        self.motorParams["Left"].pidParameters.minOutput = params["Left"]["pidParameters.minOutput"]
        self.motorParams["Left"].pidParameters.maxOutput = params["Left"]["pidParameters.maxOutput"]
        self.motorParams["Left"].pidParameters.k_p = params["Left"]["pidParameters.k_p"]
        self.motorParams["Left"].pidParameters.k_i = params["Left"]["pidParameters.k_i"]
        self.motorParams["Left"].pidParameters.k_d = params["Left"]["pidParameters.k_d"]

        self.motorParams["Right"] = self.interface.MotorAngleControllerParameters()
        self.motorParams["Right"].maxRotationAcceleration = params["Right"]["maxRotationAcceleration"]
        self.motorParams["Right"].maxRotationSpeed = params["Right"]["maxRotationSpeed"]
        self.motorParams["Right"].feedForwardGain = params["Right"]["feedForwardGain"]
        self.motorParams["Right"].minPWM = params["Right"]["minPWM"]
        self.motorParams["Right"].pidParameters.minOutput = params["Right"]["pidParameters.minOutput"]
        self.motorParams["Right"].pidParameters.maxOutput = params["Right"]["pidParameters.maxOutput"]
        self.motorParams["Right"].pidParameters.k_p = params["Right"]["pidParameters.k_p"]
        self.motorParams["Right"].pidParameters.k_i = params["Right"]["pidParameters.k_i"]
        self.motorParams["Right"].pidParameters.k_d = params["Right"]["pidParameters.k_d"]

        self.interface.setMotorAngleControllerParameters(self.motors[0], self.motorParams["Left"] )
        self.interface.setMotorAngleControllerParameters(self.motors[1], self.motorParams["Right"])

    def moveForward(self, speed):
        self.interface.setMotorRotationSpeedReferences(self.motors, [speed, speed])

    def wheel_rotate(self, angle, name):
        self.interface.startLogging("logs/Original/"+name + ".log")
        self.interface.increaseMotorAngleReferences(self.motors,[angle, angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            motorAngles = self.interface.getMotorAngles(self.motors)
            if motorAngles:
                print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
            time.sleep(0.1)
        print "Destination reached!"
        self.interface.stopLogging()


    def left90(self):
        angle = 5.0176
        resistance = 0.45
        angle += resistance
        self.interface.increaseMotorAngleReferences(self.motors, [angle, -angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            motorAngles = self.interface.getMotorAngles(self.motors)
        print "Destination reached!"

    def moveLeft(self, angle):
        pass

    def moveright(self,angle):
        self.moveLeft(-angle)

    def moveDistance(self, distance):
        C = 13.502
        loop = distance/C
        angle = loop * 2 * math.pi
        self.interface.increaseMotorAngleReferences(self.motors, [angle, angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            motorAngles = self.interface.getMotorAngles(self.motors)
        print "Destination reached!"
 
    def rotate(self, angle):
        #postive angle means turn left
        angle = angle/90 * 5.0176
        resistance = 0.5
        angle += resistance
        self.interface.increaseMotorAngleReferences(self.motors, [angle, -angle])
        while not self.interface.motorAngleReferencesReached(self.motors):
            motorAngles = self.interface.getMotorAngles(self.motors)

    def navigatieToWaypoint(self, float x, float y):

