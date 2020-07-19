"Aire d'un polygone"
import math

def decoupe_triangles(poly): #poly = liste des coord
    resultat = []
    i = 0
    for i in range(len(poly) -2):
        triangle = [poly[0], poly[i+1], poly[i+2]]
        i += 1
        resultat.append(triangle)
    return resultat


def longueur_cotes(triangle): #liste coordonnée
    resultat = [] #initialisation résultat
    triangle.append(triangle[0])
    for i in range(len(triangle) - 1):
        cote = math.sqrt((triangle[i][0] - triangle[i + 1][0])**2 + (triangle[i][1] - triangle[i + 1][1])**2)
        resultat.append(cote)
    return resultat



def calcul_aire(triangle_l): #entrée = longueurs cotés, sortie = aire du triangle
    cote1, cote2, cote3 = triangle_l[0], triangle_l[1], triangle_l[2]
    p = (cote1 + cote2 + cote3) / 2                         #p est le demi périmètre du triangle
    aire = math.sqrt (p * (p - cote1) * (p - cote2) * (p - cote3)) #formule du héron
    return aire


def aire_poly(poly): #entrée: liste coord du poly
    List_triangles = decoupe_triangles(poly)
    resultat = 0 #initialisation du résultat
    for i in range(len(List_triangles)):
        resultat += calcul_aire(longueur_cotes(List_triangles[i]))
    return resultat
