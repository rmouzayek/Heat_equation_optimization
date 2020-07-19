# -*- coding: utf-8 -*-
"""
=================================================================================
                                 Main Algorithms
=================================================================================
"""

from Vertex import *
import matlab.engine
import matplotlib.pyplot as plt
import numpy as np
from math import cos, sin, pi



# ===============================================================================
#                             Best Value of a vertex
# ===============================================================================

#   On cherche la position du sommet i qui maximise la fonctionnelle de forme
#   la fonction prend en paramètres :
#
#   - initValue : la valeur de l'intégrale du polygone initial (pour optimiser
#     et ne pas avoir à le calculer à chaque fois)
#
#   - dl : la longueur du pas
#
#   - i : le numéro du sommet
#
#   - nbTest : le nombre de valeur testée de part et d'autre du sommet, en tout
#     2*nbTest valeurs sont testées sur chaque sommet
#
#   - eng : le moteur matlab
#

def bestValue(polygon, initValue, i, nbTest, dl, eng) :

    #   On stocke les valeurs des intégrales liées à chacun des déplacements
    #   dans une liste
    #   right correspond aux déplacements à droite du point
    #   left correspond aux déplacement à gauche du point

    left = [polygon.valueIntegral(i, -j * dl, eng) for j in range(nbTest)]
    right = [polygon.valueIntegral(i, j * dl, eng) for j in range(nbTest)]
    L = np.array(left + [initValue] + right)

    #   On cherche le maximum dans cette liste, puis on trouve l'index de ce
    #   maximum, qu'on appelle indexMax
    indexMax = np.argmax(L)

    #   Le résulat retourné contient la valeur maximum de l'intégrale,
    #   et le déplacement associé à celui-ci
    return [L[indexMax], (indexMax - nbTest) * dl]

def bestValueOS(polygon, initValue, i, nbTest, dl, eng) :
    #
    #   OS : Odd Symetrical
    #   On stocke les valeurs des intégrales liées à chacun des déplacements
    #   dans une liste
    #   right correspond aux déplacements à droite du point
    #   left correspond aux déplacement à gauche du point
    #   nbTest correspond au nombre de tests de part et d'autre de chaque
    #

    left = [polygon.valueIntegral(i, -j * dl, eng) for j in range(nbTest)]
    right = [polygon.valueIntegral(i, j * dl, eng) for j in range(nbTest)]
    L = np.array(left + [initValue] + right)

    #   On cherche le maximum dans cette liste, puis on trouve l'index de ce
    #   maximum, qu'on appelle indexMax
    indexMax = np.argmax(L)

    #   Le résulat retourné contient la valeur maximum de l'intégrale,
    #   et le déplacement associé à celui-ci
    return [L[indexMax], (indexMax - nbTest) * dl]

# ===============================================================================
#                              Naive Mainloop
# ===============================================================================

#   Cette boucle naïve se contente de parcourir les sommets pour trouver le
#   meilleur déplacement possible

def naiveMainloop(polygon, dl, nbTest, initValue, nbIteration, values, eng) :
    #   Conservation des données de la temperature moyenne pour chaque itération
    #   values est une liste vide destinée à conserver les valeurs de l'intégrale

    if nbIteration == 0 :
        print("Fin de la simulation")
        return 0

    #   On cherche le petit déplacement qui maximise notre fonctionnelle
    #   de forme lors d'une itération de l'algorithme
    #   On examine chacun des sommets indépendamment

    max = [0,0]                                                     # Initialisation du maximum
    rank = 0
    for i in range(2, polygon.N) :
        val = bestValue(polygon, initValue, i, nbTest, dl, eng)
        if val[0] > max[0] :
            max = val
            rank = i

    #   Si la valeur maximum est atteinte pour un déplacement nul,
    #   on arrête la simulation
    if max[1] == 0 :
        print("Il reste " + str(nbIteration) + " itérations")
        return nbIteration

    # Sinon on bouge un sommet
    polygon.move(rank, max[1])
    values.append(max[0])

    # Appel récursive de la fonction
    naiveMainloop(polygon, dl, nbTest, max[0], nbIteration - 1, values, eng)


# ===============================================================================
#               Mainloop on Symetrical Figures with Odd number of sides
# ===============================================================================


#   Cette fois-ci, la boucle de l'algorithme est adaptée pour traiter les
#   figures symétriques, pour gagner du temps d'execution notamment.
#   On travaille d'abord avec un nombre de côtés impaires car les
#   mouvement sont beaucoup plus faciles à traiter qu'avec les polygones
#   pairs

def OSMainloop(polygon, dl, nbIteration, nbTest, eng) :

    if nbIteration == 0 :
        print("Fin de la simulation")
        return 0

    initValue = polygon.valueIntegral(0,0,eng)

    #   On cherche le petit déplacement qui maximise notre fonctionnelle
    #   de forme lors d'une itération de l'algorithme
    #   On examine chacun des sommets indépendamment

    max = [0,0]                                                     # Initialisation du maximum
    rank = 0
    for i in range(2, int((polygon.N + 3) / 2)) :
        val = bestValueOS(polygon, initValue, i, nbTest, dl, eng)
        if val[0] > max[0] :
            max = val
            rank = i

    #   S'il n'y a pas d'améliorations, on stoppe
    if max[1] == 0 :
        print("Fin de la simulation")
        return 1

    # Sinon on bouge un sommet
    polygon.move(rank, max[1])
    polygon.move(polygon.N - rank + 1, -max[1])

    # Appel récursive de la fonction
    OSMainloop(polygon, dl, nbIteration - 1, nbTest, eng)

# ===============================================================================
#            Mainloop avec exploitation de la fonction de contraction
# ===============================================================================

#   Les fonctions ci-dessous exploitent la fonction de contraction en adoptant des
#   déplacements beaucoup plus libres

def bestValueContraction(polygon, initValue, i, nbTest, r, eng) :
    """
    polygon : polygone donnée en entrée
    initValue : Valeur de l'intégrale initiale (pour ne pas la recalculer)
    nbTest : Le nombre de test
    r : longueur du déplacement
    """
    area = polygon.area()
    L = []
    for n in range(nbTest) :
        copy = polygon.deepCopy()
        dir = Vector(cos(n * 2 * pi / nbTest), sin(n * 2 * pi / nbTest))
        copy.moveFreely(i, dir, r)         # Déplacement du point
        copy.contract(area, .01)
        L = L + [copy.valueIntegral(0, 0, eng)]

    L = np.array(L)
    indexMax = np.argmax(L)
    max = L[indexMax]
    if max > initValue :
        return [max, indexMax]
    return [initValue, 'o']

def mainloopContraction(polygon, initValue, nbTest, nbIteration, r, area, values, eng) :
    """
    La fonction définie ici parcourt les sommets en effectuant des déplacements
    plus libres que dans la version naive. On exploite ici des déplacements dans des
    directions circulaires, en combinant cela avec des contractions de la figure en entier
    """
    refine = 1
    if nbIteration == 0 :
        print("Fin de la simulation")
        return nbIteration

    max = [0,0]                                                     # Initialisation du maximum
    rank = 0
    for i in range(2, polygon.N) :
        val = bestValueContraction(polygon, initValue, i, nbTest, r, eng)
        if val[0] > max[0] :
            max = val
            rank = i

    #   Si la valeur maximum est atteinte pour un déplacement nul,
    #   on arrête la simulation

    if max[1] == 'o':
        print("Plus d'amélioration. Fin de l'algorithme")
        return
    else :
        print(max)
        print(rank)
        # Sinon on bouge un sommet
        dir = Vector(cos(2 * pi * max[1] / nbTest), sin(2 * pi * max[1] / nbTest))
        polygon.moveFreely(rank, dir, r)
        polygon.contract(area, .01)
        values.append(max[0])
        mainloopContraction(polygon, max[0], nbTest, nbIteration - 1, r, area, values, eng)

# ===============================================================================
#            Mainloop avec exploitation de la fonction de contraction
#                       et exploitation des symétries
# ===============================================================================

# Il reste a corriger les éventuels cas dégénerés, lorsque le polygone
# risque de perdre son caractère convexe
def bestValueContraction_Symetry(polygon, area, initValue, i, nbTest, r, impair, pointe, eng) :
    # Si l'indice du sommet est trop grand, c'est qu'il y a une erreur
    N = polygon.N
    assert(i < N / 2 + 1)
    L = []

    # /// CAS IMPAIR ///
    if impair :
        # DEBUGGE
        if pointe :
            # Si on s'attaque au sommet, on ne peut tester que deux directions, qui
            # sont les direction à droite et à gauche sur l'axe des abscisses
            # (car sinon on casse la symétrie par rapport à cet axe)
            for n in [1, -1] :
                copy = polygon.deepCopy()
                dir = Vector(n, 0)
                copy.moveFreely(i, dir, r)         # Déplacement du point i
                copy.contract(area, .01)
                copy.plotPY('r')
                L = L + [copy.valueIntegral(0, 0, eng)]

            L = np.array(L)
            print(L)
            indexMax = np.argmax(L)
            max = L[indexMax]
            if max > initValue :
                if indexMax == 0 :
                    return [L[indexMax], '+']
                else :
                    return [L[indexMax], '-']
            else :
                return [initValue, 'o']
        # DEBUGGE
        else :
            # Si on s'occupe d'un côté qui n'est pas le sommet
            for n in range(nbTest) :
                copy = polygon.deepCopy()
                dir = Vector(cos(n * 2 * pi / nbTest), sin(n * 2 * pi / nbTest))
                dirSym = Vector(cos(n * 2 * pi / nbTest), -sin(n * 2 * pi / nbTest))
                copy.moveFreely(i, dir, r)                  # Déplacement du point i
                copy.moveFreely(N - i + 1, dirSym, r)       # Déplacement du symétrique
                copy.contract(area, .01)
                L = L + [copy.valueIntegral(0, 0, eng)]

            L = np.array(L)
            print(L)
            indexMax = np.argmax(L)
            max = L[indexMax]
            if max > initValue :
                return [L[indexMax], indexMax]
            return [initValue, 'o']

    # /// CAS PAIR ///
    else :
        for n in range(nbTest) :
            print('Enter')
            copy = polygon.deepCopy()
            dir = Vector(cos(n * 2 * pi / nbTest), sin(n * 2 * pi / nbTest))
            dirSym = Vector(cos(n * 2 * pi / nbTest), -sin(n * 2 * pi / nbTest))
            copy.moveFreely(i, dir, r)                  # Déplacement du point i
            copy.moveFreely(N - i + 1, dirSym, r)       # Déplacement du symétrique
            copy.contract(area, .01)
            copy.plotPY('r')
            plt.show()
            L = L + [copy.valueIntegral(0, 0, eng)]

        L = np.array(L)
        indexMax = np.argmax(L)
        max = L[indexMax]
        if max > initValue :
            return [L[indexMax], indexMax]
        return [initValue, 'o']

def mainloopContraction_Symetry(polygon, initValue, nbTest, nbIteration, r, area, values, eng) :
    """
    La fonction definie ici se applique l'algorithme de boucle avec contraction mais en
    exploitant les symétrie de la figure. Le polygon donné en entrée doit bien évidemment
    être symétrique pour que l'algorithme fonctionne
    """
    if nbIteration == 0 :
        return 0
    # Initialisation de la valeur de l'intégrale
    # On va devoir dissocier deux cas de figure selon que le polygon
    # possède un nombre de côtés pair ou impair
    n = polygon.N
    impair = (n % 2 != 0)  # Booléen pour savoir si le polygone est impair

    # Initialise une liste avec la liste des côtés modifiables
    sides = [i for i in range(2, int(n / 2) + int(impair))]

    max = [0,0]                            # Initialisation du maximum
    rank = 0

    for i in sides :
        # On parcourt la liste des sommets possibles
        if i == int(n / 2) + 1 and impair :
            val = bestValueContraction_Symetry(polygon, area, initValue, i, nbTest, r, impair, True, eng)
        else :
            val = bestValueContraction_Symetry(polygon, area, initValue, i, nbTest, r, impair, False, eng)

        if val[0] > max[0] :
            max = val
            rank = i

    #   Si la valeur maximum est atteinte pour un déplacement nul,
    #   on arrête la simulation
    if max[1] == 'o' :
        print("Fin de la simulation, plus d'amélioration")
        return nbIteration

    # Cas de si on manipule le sommet
    if max[1] == '+' :
        polygon.moveFreely(rank, Vector(1, 0), r)
    elif max[1] == '-' :
        polygon.moveFreely(rank, Vector(-1, 0) , r)
    else :
        # Vecteur directeur du déplacement gardé
        dir = Vector(cos(2 * pi * max[1] / nbTest), sin(2 * pi * max[1] / nbTest))
        dirSym = Vector(cos(2 * pi * max[1] / nbTest), -sin(2 * pi * max[1] / nbTest))

        #Déplacement du premier point
        polygon.moveFreely(rank, dir, r)

        # Déplacement de son symétrique (plusieurs cas)
        if impair :
            rankSym = n - rank + 1
            polygon.moveFreely(rankSym, dirSym, r)
        else :
            rankSym = n - rank
            polygon.moveFreely(rankSym, dirSym, r)

    polygon.contract(area, .01)
    values.append(max[0])
    mainloopContraction_Symetry(polygon,max[0], nbTest, nbIteration - 1, r, area, values, eng)

# ===============================================================================
#                       Mainloop avec inspiration circulaire
# ===============================================================================

def mainloopCirc(polygon, nbIteration, dl, area, values, eng) :

    return 0

#   Idées à faire pour le developpement du code :
#
#   @ Exploitation des symétries
