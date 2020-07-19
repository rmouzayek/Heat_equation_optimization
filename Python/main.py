from Vertex import *
from Polygon_Optimization import *
import matplotlib.pyplot as plt
import math as m
import numpy as np
import matlab.engine
import time
from colours_module import *

eng = matlab.engine.start_matlab()
L = linear_gradient("#0000FF", "#ff0000", n=1000)



for k in range(25) :
    # Génération du polygone
    P = gen_poly(5)
    P = list2poly(P)
    P.contract(5, 0.01)
    plt.subplot(5,5,k+1)
    # On va calculer l'intégrale
    value = max(0, int(P.valueIntegral(0, 0, eng)) - 800)
    print(value)
    P.plotPY(L[value])
plt.show()






#S.plotPY('b')
#V.plotPY('r')
#W.plotPY('g')
#plt.show()
#S.plotPY('r')
#plt.show()





"""


print(P.valueIntegral(0, 0, eng))
print(P.area())
P.plotPY('g')
plt.show()
# Tracé initial et stockage de la valeur de l'intégrale initiale

start = time.clock()
initMean = P.valueIntegral(0,0,eng)             # Valeur initiale
initArea = P.area()


values = []
# Boucle principale
naiveMainloop(P, 0.1, 2, 5, values, eng)
print(values)


endMean = P.valueIntegral(0,0,eng)             # Valeur finale
endArea = P.area()

print("Valeur initiale : " + str(initMean))
print("Valeur finale : " + str(endMean))
print("Aire initiale : " + str(initArea))
print("Aire finale : " + str(endArea))

# Affichage temps de simulation
end = time.clock()
print("\nTemps de la simulation " + str(end - start))


# Tracé final
P.plotPY('b')
plt.show()

"""
