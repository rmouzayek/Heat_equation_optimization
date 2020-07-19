"""
======================================================================
                        Script de simulation
======================================================================
"""
from Vertex import *
from Polygon_Optimization import *
import matlab.engine

eng = matlab.engine.start_matlab()

# Création du fichier de Sauvegarde
import os
os.chdir("/Users/viviertanguy/Documents/GitHub/Projet-2A/Simulations")
resultat = open("comparaison_22.txt", "w")

# Entete
resultat.write("======================================================================\n")
resultat.write("              Simulation 1 - Comparaison de deux methodes\n")
resultat.write("======================================================================\n\n\n")

P = gen_poly(5)
S = list2poly(P)
S.plotPY('y')
plt.show()

S.plotPY('y')
K = S.deepCopy()
area = S.area()

init = S.valueIntegral(0, 0, eng)


resultat.write("*********************** ALGO NAIF ****************************\n")
resultat.write("dl = 0.1, NBTEST = 1\n")
resultat.write("Polygone d'entree d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Initiale : " + str(S.area()) + "\n")
resultat.write("Methode iterative souple pour 100 itérations maximum \n\n")
values = []
naiveMainloop(S, 0.1, 1, init, 20, values, eng)
resultat.write("Polygone de sortie d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Finale : " + str(S.area()) + "\n")
resultat.write("Nombre d'iterations : " + str(len(values)) + "\n")
resultat.write("Valeurs après chaque itération : " + str(values) + "\n\n")
S.plotPY('r')

# ---------------------------------------------------------------------------
S = K.deepCopy()
resultat.write("*********************** ALGO SOUPLE ****************************\n")
resultat.write("r = 0.05, NBTEST = 8\n")
resultat.write("Polygone d'entree d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Initiale : " + str(S.area()) + "\n")
resultat.write("Methode iterative souple pour 100 itérations maximum \n\n")
values = []
mainloopContraction(S, init, 8, 20, 0.1, area, values, eng)
resultat.write("Polygone de sortie d'algorithme SOUPLE : \n " + S.__str__() + "\n")
resultat.write("Aire Finale : " + str(S.area()) + "\n")
resultat.write("Nombre d'iterations : " + str(len(values)) + "\n")
resultat.write("Valeurs après chaque itération : " + str(values) + "\n\n")
S.plotPY('b')

resultat.close()

plt.show()
