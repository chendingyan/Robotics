import time
import sys
import random
import math


def getInitialX():
    num = random.randint(10, 50)
    return num


def getInitialY():
    num = random.randint(10, 50)
    return num


def Forward(x, y, theta, D, e, f):
    xnew = x + (D + e) * math.cos(math.radians(theta))
    ynew = y + (D + e) * math.sin(math.radians(theta))
    thetanew = theta + f
    return xnew, ynew, thetanew


def Rotate(x, y, theta, alpha, g):
    xnew = x
    ynew = y
    thetanew = theta + alpha + g
    return xnew, ynew, thetanew


def getRandomTheta():
    theta = 0
    return theta


def DrawLines():
    line1 = (10, 10, 10, 500)  # (x0, y0, x1, y1)
    line2 = (10, 10, 500, 10)  # (x0, y0, x1, y1)
    print "drawLine:" + str(line1)
    print "drawLine:" + str(line2)


def run():
    numberOfParticles = 100
    particles = [(100, 100, getRandomTheta()) for i in range(numberOfParticles)]
    print "drawParticles:" + str(particles)
    time.sleep(0.5)
    mu = 0
    sigma = 3
    e = random.gauss(mu, sigma)

    for c in range(10):
        particles = [(Forward(particles[i][0], particles[i][1], particles[i][2], 300, random.gauss(0, 3), random.gauss(0, 2))) for i
            in range(numberOfParticles)]
        print "drawParticles:" + str(particles)
        time.sleep(0.5)
        particles = [(Rotate(particles[i][0], particles[i][1], particles[i][2], 90, random.gauss(0, 2))) for i in
                     range(numberOfParticles)]
        print "drawParticles:" + str(particles)
        time.sleep(0.5)

#
# for i in range(numberOfParticles):

#


# while c < 5:
# curr_X = getRandomX()
# curr_Y = getRandomY()
# curr_Theta = getRandomTheta()
# Create a list of particles to draw. This list should be filled by tuples (x, y, theta).
# particles = [(getRandomX(),getRandomY(), getRandomTheta()) for i in range(numberOfParticles)]
# print "drawParticles:" + str(particles)

# c += 1;
# time.sleep(0.5)



