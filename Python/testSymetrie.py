from Vertex import *
from Polygon_Optimization import *
import matplotlib.pyplot as plt
import math as m
import numpy as np
import matlab.engine
import time
eng = matlab.engine.start_matlab()

s1 = Vertex(0,-1)
s2 = Vertex(0,1)
s3 = Vertex(2,1.5)
s4 = Vertex(3,0)
s5 = Vertex(2,-1.5)
S = Polygon(s1, s2, s3, s4, s5)

area = S.area()
initValue = S.valueIntegral(0, 0, eng)
print(initValue)
values = []
mainloopContraction_Symetry(S, 8, 20, .1, area, values, eng)
S.plotPY('r')
plt.show()
