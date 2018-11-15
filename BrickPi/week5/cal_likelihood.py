import math
import numpy as np
import time
import random
import brickpi
from Utility import Car

port = 3
interface = brickpi.Interface()
interface.initialize()
interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC);

Robot = Car(interface)
# points
p_O = [0, 0]
p_A = [0, 168]
p_B = [84, 168]
p_C = [84, 126]
p_D = [84, 210]
p_E = [168, 210]
p_F = [168, 84]
p_G = [210, 84]
p_H = [210, 0]

# walls
w_a = [p_O, p_A, "O-A"]
w_b = [p_A, p_B, "A-B"]
w_c = [p_C, p_D, "C-D"]
w_d = [p_D, p_E, "D-E"]
w_e = [p_E, p_F, "E-F"]
w_f = [p_F, p_G, "F-G"]
w_g = [p_G, p_H, "G-H"]
w_h = [p_H, p_O, "H-O"]

list_wall = [w_a, w_b, w_c, w_d, w_e, w_f, w_g, w_h]


# Functions to generate some dummy particles data:
def calcX(cx):
    return random.gauss(cx, 3)  # in cm


def calcY(cy):
    return random.gauss(cy, 3)  # in cm


def calcW():
    return random.random()


def calcTheta(ct):
    return random.gauss(ct, 2)


# A Canvas class for drawing a map and particles:
#     - it takes care of a proper scaling and coordinate transformation between
#      the map frame of reference (in cm) and the display (in pixels)
class Canvas:
    def __init__(self, map_size=210):
        self.map_size = map_size  # in cm
        self.canvas_size = 768  # in pixels
        self.margin = 0.05 * map_size
        self.scale = self.canvas_size / (map_size + 2 * self.margin)

    def drawLine(self, line):
        x1 = self.__screenX(line[0])
        y1 = self.__screenY(line[1])
        x2 = self.__screenX(line[2])
        y2 = self.__screenY(line[3])
        print "drawLine:" + str((x1, y1, x2, y2))

    def drawParticles(self, data):
        display = [(self.__screenX(d[0]), self.__screenY(d[1])) + d[2:] for d in data]
        print "drawParticles:" + str(display)

    def __screenX(self, x):
        return (x + self.margin) * self.scale

    def __screenY(self, y):
        return (self.map_size + self.margin - y) * self.scale


# A Map class containing walls
class Map:
    def __init__(self):
        self.walls = []

    def add_wall(self, wall):
        self.walls.append(wall)

    def clear(self):
        self.walls = []

    def draw(self):
        for wall in self.walls:
            canvas.drawLine(wall)


# Simple Particles set
class Particles:
    def __init__(self):
        self.n = 100
        self.data = []

    def setNum_particles(self, num):
        self.n = num

    def update(self):
        self.data = [(calcX(Robot.current_x), calcY(Robot.current_y), calcTheta(Robot.current_theta), calcW()) for i in
                     range(self.n)]

    def update_w(self, w):
        pass

    def draw(self):
        canvas.drawParticles(self.data)


def find_mm(angle_list):
    min = 370
    max = -370
    for item in angle_list:
        if item > 0 and item < min:
            min = item
        elif item < 0 and item > max:
            max = item
    if max == -370:
        max = 0
        for item in angle_list:
            if item > max:
                max = item
    elif min == 370:
        min = 0
        for item in angle_list:
            if item < min:
                min = item
    return min, max


def find_point_index(point_list, angle_list, min, max):
    min_index = angle_list.index(min)
    max_index = angle_list.index(max)
    if abs(max_index - min_index) == 1:
        return point_list[max_index], point_list[min_index]
    elif (max_index == 2 and min_index == 4) or (max_index == 2 and min_index == 4):
        return point_list[max_index], point_list[min_index]
    elif (max_index == 0 and min_index == 8) or (max_index == 8 and min_index == 0):
        return point_list[max_index], point_list[min_index]
    else:
        angle_list[max_index] = -370
        min, max = find_mm(angle_list)
        return find_point_index(point_list, angle_list, min, max)


def find_walls(x, y, theta):
    possible_w = list()
    max_angle = 0
    point_list = [p_O, p_A, p_B, p_C, p_D, p_E, p_F, p_G, p_H]
    angle_list = list()
    for item in point_list:
        angle = math.atan2(item[1] - y, item[0] - x)
        angle = math.degrees(angle) % 360
        angle_list.append(angle)
        if angle > max_angle:
            max_angle = angle
    res = 360 - max_angle

    for i in range(len(angle_list)):
        angle_list[i] -= theta

    min, max = find_mm(angle_list)
    p1, p2 = find_point_index(point_list, angle_list, min, max)
    return p1, p2


def decide_walls():
    pass


def calculate_m(x, y, theta, s_read, particle_data):
    const_K = 0  # a constant K added as its tail (lecture notes p21)
    pt1, pt2 = find_walls(x, y, theta)
    m = list()
    likelihood = list()
    zm = list()
    for i in range(len(particle_data)):
        den_m = (pt2[1] - pt1[1]) * math.cos(math.radians(theta)) - (pt2[0] - pt1[0]) * math.sin(math.radians(theta))
        num_m = (pt2[1] - pt1[1]) * (pt1[0] - particle_data[i][0]) - (pt2[0] - pt1[0]) * (pt1[1] - particle_data[i][1])
        m.append(num_m / den_m)
        zm.append(s_read[0] - m[i])
    sigma_s = (max(zm) - min(zm)) / 2 * 0.34
    # print("actual distance to the wall m =", m)

    for i in range(len(particle_data)):
        likelihood.append(math.exp(-((s_read[0] - m[i]) ** 2) / (2 * (sigma_s ** 2))))
        # print(((45 - m[i]) ** 2) , "++" , (2 * (sigma_s ** 2)))
    const_K = 0.01 * max(likelihood)
    for i in range(len(particle_data)):
        likelihood[i] = likelihood[i] + const_K
    return likelihood


def obtain_z():
    usReading = interface.getSensorValue(port)
    if usReading:
        return usReading
    else:
        print "Failed US reading"


def normalize(likelihood):
    sum_likelihood = sum(likelihood)
    for i in range(len(likelihood)):
        likelihood[i] = (likelihood[i] / sum_likelihood) * 100
    return likelihood
    # print(likelihood)
    # print(sum(likelihood))
    # print(max(likelihood))


def resampling(likelihood):
    prob = list()
    index_list = list()
    current_pointer = 0
    for i in range(len(likelihood)):
        current_pointer += likelihood[i]
        prob.append(current_pointer)
    for i in range(len(likelihood)):
        rand = random.uniform(0, 100)
        for j in range(len(prob)):
            if (rand - prob[j] <= 0):
                index_list.append(j)
                break
    return index_list


if __name__ == "__main__":
    canvas = Canvas()  # global canvas we are going to draw on

    mymap = Map()
    # Definitions of walls
    # a: O to A
    # b: A to B
    # c: C to D
    # d: D to E
    # e: E to F
    # f: F to G
    # g: G to H
    # h: H to O
    mymap.add_wall((0, 0, 0, 168))  # a
    mymap.add_wall((0, 168, 84, 168))  # b
    mymap.add_wall((84, 126, 84, 210))  # c
    mymap.add_wall((84, 210, 168, 210))  # d
    mymap.add_wall((168, 210, 168, 84))  # e
    mymap.add_wall((168, 84, 210, 84))  # f
    mymap.add_wall((210, 84, 210, 0))  # g
    mymap.add_wall((210, 0, 0, 0))  # h
    mymap.draw()
    Robot.current_x = 158
    Robot.current_y = 10
    Robot.current_theta = 0
    particles = Particles()
    t = 0.5
    particles.update()
    particles.draw()
    likelihood = calculate_m(Robot.current_x, Robot.current_y, Robot.current_theta, obtain_z(), particles.data)
    likelihood = normalize(likelihood)
    index_list = resampling(likelihood)
    new_particles = Particles()
    new_particles.update()
    for i in range(0, particles.n):
        new_particles.data[i] = particles.data[index_list[i]]
        list1 = list(new_particles.data[i])
        list1[2] = 0.01
        new_particles.data[i] = tuple(list1)

    print(new_particles.data)
    time.sleep(1)
    new_particles.draw()

