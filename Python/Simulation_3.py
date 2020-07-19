"""
======================================================================
                        Script de simulation
                            COMPARAISON
======================================================================
"""
from Vertex import *
from Polygon_Optimization import *
import matlab.engine
import matplotlib.pyplot as plt

eng = matlab.engine.start_matlab()

# Création du fichier de Sauvegarde
import os
os.chdir("/Users/viviertanguy/Documents/GitHub/Projet-2A/Simulations")
resultat = open("resultat_souple_regulier.txt", "w")

# ---------------------------------------------------------------------------
S = gen_poly(5)
S = list2poly(S)
S.contract(5, 0.01)
S.plotPY('b')
plt.show()
S.plotPY('y')
resultat.write("*********************** ALGO SOUPLE ****************************\n")
resultat.write("r = 0.1, NBTEST = 8\n")
resultat.write("Polygone d'entree d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Initiale : " + str(S.area()) + "\n")
resultat.write("Symetrie Initiale : " + str(S.degSymetrie(1000)) + "\n")
resultat.write("Methode iterative symétrique souple pour 100 itérations maximum \n\n")
values = []
mainloopContraction(S, 8, 50, .1, 2.5, values, eng)
S.plotPY('r')



resultat.close()
plt.show()
