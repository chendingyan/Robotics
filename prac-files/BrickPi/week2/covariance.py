import math
import pandas as pd
import numpy as np


def main(logfile):
    data = np.array([[0.84,-1.08],
             [-0.65,-1.21],
             [1.55,0.92],
             [1.31,1.10],
             [1.18,1.60],
             [1.70,1.38],
             [1.87,1.25],
             [2.05,1.05],
             [2.21,2.21],
             [2.78,2.10]])
    print(data[:,1])
    print ("Mean of X: {}".format(np.mean(data[:,0])))
    print ("Mean of Y: {}".format(np.mean(data[:,1])))
    data = np.vstack((data[:,0],data[:,1]))
    print("Covariance:")
    print(np.cov(data))


if __name__ == '__main__':
    main("final_pos.log")