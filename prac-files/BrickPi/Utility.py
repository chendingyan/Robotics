import brickpi
import time
import json
import math
class Car:
    def __init__(self, interface, config_file='carpet_params.json', touch_ports = None, ultrasonic_port = None):
        self.interface = interface
        self.wheel_diameter = 4.3 #cm
        self.circumference = self.wheel_diameter * math.pi
        self.distance = 0
        # self.pose = 0
        # self.ultra_pose = 0
        self.motor_speeds = [0,0]
        # self.left_speed = 0
        # self.right_speed = 0
        # self.top_speed = 0
        self.motors = [0,2,3]
        self.motorParams = {}
        self.interface.motorEnable(self.motors[0])
        self.interface.motorEnable(self.motors[1])
        self.interface.motorEnable(self.motors[2])

        # Import parameters
        params = None
        with open(config_file, "r") as f:
            params = json.load(f)
        if params is None:
            raise Exception("No configuration file!")
        self.distance_calibration = params["distance_calibration"]
        self.angle_calibration = params["angle_calibration"]
        self.ultra_angle_calibration = params["ultra_angle_calibration"]

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

        self.motorParams["Top"] = self.interface.MotorAngleControllerParameters()
        self.motorParams["Top"].maxRotationAcceleration = params["Top"]["maxRotationAcceleration"]
        self.motorParams["Top"].maxRotationSpeed = params["Top"]["maxRotationSpeed"]
        self.motorParams["Top"].feedForwardGain = params["Top"]["feedForwardGain"]
        self.motorParams["Top"].minPWM = params["Top"]["minPWM"]
        self.motorParams["Top"].pidParameters.minOutput = params["Top"]["pidParameters.minOutput"]
        self.motorParams["Top"].pidParameters.maxOutput = params["Top"]["pidParameters.maxOutput"]
        self.motorParams["Top"].pidParameters.k_p = params["Top"]["pidParameters.k_p"]
        self.motorParams["Top"].pidParameters.k_i = params["Top"]["pidParameters.k_i"]
        self.motorParams["Top"].pidParameters.k_d = params["Top"]["pidParameters.k_d"]

        self.interface.setMotorAngleControllerParameters(self.motors[0], self.motorParams["Left"] )
        self.interface.setMotorAngleControllerParameters(self.motors[1], self.motorParams["Right"])
        self.interface.setMotorAngleControllerParameters(self.motors[2], self.motorParams["Top"])

        # self.calibrate_ultra_position()
        # self.interface.setMotorRotationSpeedReferences(self.motors, self.left_speed, self.right_speed)
        self.touch_ports = touch_ports
        if self.touch_ports is not None:
            for i in touch_ports:
                self.interface.sensorEnable(i , brickpi.SensorType.SENSOR_TOUCH)

        self.ultrasonic_port = ultrasonic_port
        if self.ultrasonic_port is not None:
            for i in touch_ports:
                self.interface.sensorEnable(i, brickpi.SensorType.SENSOR_ULTRASONIC)




    def read_touch_sensor(self, port):
        if self.touch_ports is not None:
            result = self.interface.getSensorValue(port)
            if result:
                return result[0]
            else:
                raise Exception("Touch sensor not initialized!")

    def read_ultrasonic_sensor(self, port):
        if self.ultrasonic_port is not None:
            result = self.interface.getSensorValue(port)
            if result:
                return result
            else:
                raise Exception("Ultrasonic sensor not initialized!")

    def move_specific_wheel(self, distances= [1,1], wheels= [0,2]):
        print("Distance to move: {}".format(distances))

        motorAngles_start = self.interface.getMotorAngles(wheels)
        print("Start motor angle: {}".format(motorAngles_start))

        # Set the reference angles to reach
        circular_distances = [round((2 * x * self.distance_calibration) / self.circumference, 2) for x in distances]
        print("Distance in radians: {}".format(circular_distances))
        motorAngles_end = []

        motorAngles_end.append(round(motorAngles_start[0][0] + circular_distances[0], 2))
        motorAngles_end.append(round(motorAngles_start[1][0] + circular_distances[1], 2))
        print("Angles to end at: {}".format(motorAngles_end))

        self.interface.increaseMotorAngleReferences(wheels, circular_distances)

        # This function does PID control until angle references are reached
        while not self.interface.motorAngleReferencesReached(wheels):
            # time.sleep(0.1)
            # print(self.interface.getMotorAngles(wheels))
            if (round(self.interface.getMotorAngles(wheels)[0][0], 2) == motorAngles_end[0] or round(
                    self.interface.getMotorAngles(wheels)[1][0], 2) == motorAngles_end[1]):
                return True
            return True

    def rotate_ultrasonic_motor(self, angle):
        print("Starting reference angles: {}".format(self.interface.getMotorAngles(self.motors)))
        self.interface.increaseMotorAngleReferences(self.motors[2], angle*self.ultra_angle_calibration)

        while not self.interface.motorAngleReferencesReached(self.motors):
            pass
        print("Ending reference angles: {}".format(self.interface.getMotorAngles(self.motors)))
        return True

    def moveForward(self, distance):
        # self.interface.setMotorRotationSpeedReferences(self.motors, [speed, speed])
        return self.move_specific_wheel([distance, distance], self.motors)

    def moveLeft(self, angle):
        #According to the distance!!!
        dist = self.angle_calibration * angle
        # self.state["pose"] = self.state.get("pose", 0) + angle
        # self.save_state()
        return self.move_specific_wheel([dist, -dist])

    def moveright(self,angle):
        return self.moveLeft(-angle)

    def stop(self):
        self.interface.setMotorPwm(self.motors[0],0)
        self.interface.setMotorPwm(self.motors[1],0)

    # Developing methods
    # def calibrate_ultra_position(self):
    #     # Get current motor angle
    #     motor_angle = self.interface.getMotorAngles([2])[0][0]
    #     print("Calibration ultra position, motor angle = {}".format(motor_angle))
    #
    #     # Could calibrate to the nearest angle instead of always to zero
    #     # Right now, calculate difference between current and zero and rotate to there
    #     rotation = round(self.ultra_calibration.get(0) - motor_angle, 2)
    #
    #     print("Rotation required: {}".format(rotation))
    #     self.interface.increaseMotorAngleReferences([2], [rotation])
    #     while not self.interface.motorAngleReferencesReached([2]):
    #         pass
    #     self.state["ultra_pose"] = 0
    #     return True
    #
    # def save_state(self, state_file="robot_state.json"):
    #     with open("robot_state.json", "w") as f:
    #         json.dump(self.state, f)
    #
    # # Top ultrasonic sensor should match the pose
    # def set_ultra_pose(self, pose):
    #     print("Current ultra pose: {}".format(self.state.get("ultra_pose", -1)))
    #     # Limits on pose settings so that it doesn't overrotate and stretch the cable
    #     while pose > 360:
    #         pose -= 360
    #     while pose < -360:
    #         pose += 360
    #     if pose == 360:
    #         pose = 0
    #     if pose > 180:
    #         # If greater than 180 e.g. 270, turn it into -90
    #         pose -= 360
    #     if pose < -180:
    #         # If less than -180, e.g. -270, turn it into +90
    #         pose += 360
    #
    #     rotation = pose - self.state.get("ultra_pose", 0)
    #     if rotation:
    #         self.rotate_ultrasonic_motor(rotation)
    #         self.state["ultra_pose"] = pose
    #         self.save_state()
    #     else:
    #         print("No rotation required.")
    #     return True
    #
    # # Move the robot to the specified pose
    # def set_robot_pose(self, s_pose):
    #     print("Starting pose: {}".format(self.state.get("pose", -1)))
    #     while s_pose > 360:
    #         s_pose -= 360
    #
    #     rotation = s_pose - self.state.get("pose", 0)
    #     if rotation == 0:
    #         print("No rotation required.")
    #         return True
    #     if rotation > 180:
    #         self.moveright(rotation - 360)
    #     else:
    #         self.moveright(rotation)
    #     self.state["pose"] = s_pose
    #     print("Ending pose: {}".format(s_pose))
    #     self.save_state()
    #     return True

    # Deprecated Methods:
    # def moveDistance(self, distance):
    #     C = 13.502
    #     loop = distance/C
    #     angle = loop * 2 * math.pi
    #     self.interface.increaseMotorAngleReferences(self.motors, [angle, angle])
    #     while not self.interface.motorAngleReferencesReached(self.motors):
    #         motorAngles = self.interface.getMotorAngles(self.motors)
    #     print "Destination reached!"
    #
    # def rotate(self, angle):
    #     #postive angle means turn left
    #     angle = angle/90 * 5.0176
    #     resistance = 0.5
    #     angle += resistance
    #     self.interface.increaseMotorAngleReferences(self.motors, [angle, -angle])
    #     while not self.interface.motorAngleReferencesReached(self.motors):
    #         motorAngles = self.interface.getMotorAngles(self.motors)
    #
    # def wheel_rotate(self, angle, name):
    #     self.interface.startLogging("logs/Original/"+name + ".log")
    #     self.interface.increaseMotorAngleReferences(self.motors,[angle, angle])
    #     while not self.interface.motorAngleReferencesReached(self.motors):
    #         motorAngles = self.interface.getMotorAngles(self.motors)
    #         if motorAngles:
    #             print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
    #         time.sleep(0.1)
    #     print "Destination reached!"
    #     self.interface.stopLogging()
    # def left90(self):
    #
    #     angle = 5.0176
    #     resistance = 0.45
    #     angle += resistance
    #     self.interface.increaseMotorAngleReferences(self.motors, [angle, -angle])
    #     while not self.interface.motorAngleReferencesReached(self.motors):
    #         motorAngles = self.interface.getMotorAngles(self.motors)
    #     print "Destination reached!"
