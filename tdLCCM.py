#Implementation of 2D-LCCM proposed by Zhao et al.
#Caleb Bessit
#26 December 2023

import math
import numpy as np

def f(x, y,mu, gain):    
    a_star = math.cos( beta(y,mu)*math.acos(x) )
    b_star = math.cos( beta(x,mu)*math.acos(y) )
    return a_star*gain - math.floor(a_star*gain),  b_star*gain - math.floor(b_star*gain)

#Defines variable parameter for Chebyshev input
def beta(i,mu):
    return math.exp(mu*i*(1-i))

'''
Generates iteration number of terms of the 2D-LCCM map.
iterations  - number of terms to generate. Discards first 1000 terms to allow transient to decay
x_0, y_0    - intitial point
mu, k       - parameters
'''
def generateTerms(iterations, x_0=0.1, y_0=0.2,mu=8, k=8):
    x, y = x_0, y_0
    gain = math.pow(10,k)

    for j in range(1000):
        x, y = f(x,y,mu,k)

    xvals, yvals = np.empty(iterations), np.empty(iterations)
    for j in range(iterations):
        x, y = f(x,y,mu,gain)
        xvals[j], yvals[j] = x, y
    return xvals, yvals