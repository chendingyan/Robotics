import brickpi
import time
import sys
from BrickPi.Utility import Car
import newFile
import random
interface=brickpi.Interface()
interface.initialize()
sonar_port = None
touch_port = None
Robot = Car(interface, config_file='carpet_params.json')
distance = 10
newFile.DrawLines()
e = 0
f = 0
numberOfParticles = 100
particles = [(0, 0, 0) for i in range(numberOfParticles)]
print "drawParticles:" + str(particles)
angle = 90
for i in range(4):
    for j in range(4):
        Robot.moveForward(distance)
        particles = [
            (newFile.Forward(particles[i][0], particles[i][1], particles[i][2], distance, random.gauss(0, 3),
                             random.gauss(0, 2))) for i in range(numberOfParticles)]
        print "drawParticles:" + str(particles)
        time.sleep(0.5)
    Robot.moveright(angle)
    particles = [(newFile.Rotate(particles[i][0], particles[i][1], particles[i][2], angle, random.gauss(0, 2)))
                 for i in range(numberOfParticles)]
    print "drawParticles:" + str(particles)
    time.sleep(0.5)


interface.terminate()
