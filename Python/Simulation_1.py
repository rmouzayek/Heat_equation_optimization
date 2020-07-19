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
resultat = open("resultat_symetrie_1.txt", "w")

# Entete
resultat.write("======================================================================\n")
resultat.write("              Simulation 1ter - Symétrie \n")
resultat.write("======================================================================\n\n\n")

s1 = Vertex(0,-1)
s2 = Vertex(0,1)
s3 = Vertex(2,1.5)
s4 = Vertex(2.5,0)
s5 = Vertex(2,-1.5)
S = Polygon(s1, s2, s3, s4, s5)
S.contract(5.75, 0.01)
S.plotPY('y')
K = S.deepCopy()
area = S.area()

# ---------------------------------------------------------------------------
S = K.deepCopy()
resultat.write("*********************** ALGO SOUPLE ****************************\n")
resultat.write("r = 0.05, NBTEST = 4\n")
resultat.write("Polygone d'entree d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Initiale : " + str(S.area()) + "\n")
resultat.write("Methode iterative symétrique souple pour 100 itérations maximum \n\n")
values = []
mainloopContraction_Symetry(S, 8, 100, .1, 5.75, values, eng)
S.plotPY('b')
resultat.write("Polygone de sortie d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Finale : " + str(S.area()) + "\n")
resultat.write("Nombre d'iterations : " + str(len(values)) + "\n")
resultat.write("Valeurs après chaque itération : " + str(values) + "\n\n")

resultat.close()

plt.show()
