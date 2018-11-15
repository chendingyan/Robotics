import random

distances = 100.0
calibration = 3.0
circumference = 10.0
cd = [round((2*x*calibration)/circumference,2) for x in distances]
print(cd)