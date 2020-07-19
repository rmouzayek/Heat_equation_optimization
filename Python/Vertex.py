# -*- coding: utf-8 -*-
# ======================================================================
#              Definition des classes Vertex et Polygon
# ======================================================================

from deg_defaut_sym import *
from aire_polygone import *
import matplotlib.pyplot as plt
import matlab.engine


class Vector :

    """ Représente un vecteur """

    def __init__(self,x,y) :
        self.x = x
        self.y = y

    def __str__(self) :
        return ("v(%f,%f)" % ( self.x, self.y))


    # Normalise le vecteur
    def normalize(self) :
        norm = (self.x ** 2 + self.y ** 2) ** 0.5
        self.x = self.x / norm
        self.y = self.y / norm




class Vertex :

    """
     La classe Vertex est une classe qui représente les coordonnées des points
     d'un polygone donné

    """

    def __init__(self, x, y) :

        self.x = x
        self.y = y

    def __str__(self) :
        return ("(%f,%f)" % (self.x, self.y) )

    def __copy__(self, vertex) :
        self.x = vertex.x
        self.y = vertex.y

    def deepCopy(self) :
        copy = Vertex(0,0)
        copy.x = self.x
        copy.y = self.y
        return copy

    #-------------------------------------------------------------------
    # Déplace le sommet de dx selon x et dy selon y

    def update(self, dx, dy) :
        self.x += dx
        self.y += dy


    #-------------------------------------------------------------------
    # déplace le point dans la direction du vecteur unitaire vector

    def move(self, vector, dl) :
        # On déplace le point selon le vecteur
        dx = dl * vector.x
        dy = dl * vector.y
        self.update(dx, dy)


class Polygon :

    """
        La classe Polygon contient des Vertex (Sommets). L'ensemble de ces sommets
        forme un polygon

        Les attributs de cette classe sont :
           N : le nombre de côtés
           vertices : la liste contenant les sommets

    """

    def __init__(self, *args) :
        # Nombre de côtés dans le polygone
        self.N = len(args)

        # Liste contenant les sommets (vertex)
        self.vertices = []
        for vertex in args :
            self.vertices.append(vertex)

    def deepCopy(self):
        copy = Polygon()
        copy.N = self.N
        for vertex in self.vertices :
            copy.vertices.append(vertex.deepCopy())
        return copy


    # Print
    def __str__(self) :
        res = "class Polygon : [ "
        for vertex in self.vertices :
            res = res + vertex.__str__() + ","
        return res[:-1]+' ]'


    #------------------------------------------------------------------------------------
    # Retourne les coordonnées x et y d'un sommet
    #
    # Retourne la coordonnée x du sommet i
    def getx(self, i) :
        return self.vertices[i % self.N].x

    # Retourne la coordonnée y du sommet i
    def gety(self, i) :
        return self.vertices[i % self.N].y



    #----------------------------------------------------------------------------
    # La fonction findCoef renvoie le coefficient directeur de la droite passant
    # par les sommets i-1 et i+1

    def directorVertice(self, i) :
        dx = self.getx(i + 1) - self.getx(i - 1)
        dy = self.gety(i + 1) - self.gety(i - 1)
        res = Vector(dx, dy)
        res.normalize()
        return res



    #----------------------------------------------------------------------------
    # calcule le vecteur directeur de la droite passant par le côté i
    def directorSide(self, i) :
        dy = self.gety(i + 1) - self.gety(i)
        dx = self.getx(i + 1) - self.getx(i)
        res = Vector(dx, dy)
        res.normalize()
        return res


    #----------------------------------------------------------------------------
    # Cette méthode construit une géométrie prête à l'exportation sous matlab

    def buildGeometry(self) :

        #    On initialise une liste avec l'argument 2, qui est le code correspondant
        #    a une forme polygonale sous matlab, et self._N est le nombre de côtés
        #    Cette fonction renvoie une matrice prête a être employée dans la fonction
        #    Matlab decsg(mat)

        mat = [[2], [self.N]]
        for vertex in self.vertices :
            mat.append([vertex.x])
        for vertex in self.vertices :
            mat.append([vertex.y])
        return mat

    #----------------------------------------------------------------------------
    #
    #    Déplacement d'un point du polygone selon l'algorithme
    #    i correspond au numéro du sommet et dl à la longueur du déplacement

    def move(self, i, dl) :
        vector = self.directorVertice(i)
        self.vertices[i % self.N].move(vector, dl)

    #----------------------------------------------------------------------------
    #
    #    Déplacement d'un point du polygone
    #    i correspond au numéro du sommet et dl à la longueur du déplacement
    #    vector correspond au vecteur de déplacement

    def moveFreely(self, i, vector, dl) :
        self.vertices[i % self.N].move(vector, dl)


    #------------------------------------------------------------------------------------
    #
    #    Calcul de la valeur de l'intégrale pour un déplacement
    #    du sommet i d'une longueur dl. La méthode ne modifie ainsi
    #    pas le polygone lorsque elle est executée

    def valueIntegral(self, i, dl, eng) :
        self.move(i, dl)
        mat = matlab.double(self.buildGeometry())
        value = eng.computeIntegral(mat)
        self.move(i, -dl)
        return value


    #------------------------------------------------------------------------------------
    #
    #   La fontion calcul calcul aussi l'intégrale, mais pour un
    #   un déplacement symétrique du polygone symétrique à côtés
    #   impairs (On exploite donc la symétrie)

    def valueIntegralOS(self, i, dl, eng) :
        self.move(i, dl)
        self.move(self.N - i, -dl)
        mat = matlab.double(self.buildGeometry())
        value = eng.computeIntegral(mat)
        self.move(i, -dl)
        self.move(self.N - i + 1, dl)
        return value


    #------------------------------------------------------------------------------------
    # Fonction de traçage

    def plotPY(self,color) :

        for k in range(self.N) :
            plt.plot([self.vertices[ k % self.N].x,
                      self.vertices[(k + 1) % self.N].x],
                     [self.vertices[k % self.N].y,
                      self.vertices[(k + 1) % self.N].y],
                     color
                     )
            plt.axis([-0.5, 5, -3, 3])
            plt.axis('off')

        #plt.show()


    #------------------------------------------------------------------------------------
    # Retourne l'air du polygone

    def area(self) :

        poly = [[self.getx(i), self.gety(i)] for i in range(self.N)]
        return aire_poly(poly)

    #------------------------------------------------------------------------------------
    # Retourne l'air du polygone

    def degSymetrie(self, step) :

        poly = [[self.getx(i), self.gety(i)] for i in range(self.N)]
        return deg_sym(poly, step)


    #------------------------------------------------------------------------------------
    def contract(self, area, error) :
        """
        Contracte la figure selon l'axe des abscisses de sorte à ce qu'elle atteigne
        l'aide donnée en argument

        area : aire à obtenir en fin d'algorithme
        error : erreur maximale
        """

        lastArea = self.area()                  # Aire initiale
        step = .1
        right = Vector(1, 0)
        left = Vector(-1, 0)


        while abs(self.area() - area) > error :
            if (lastArea - area) * (self.area() - area) < 0 :
                # Si on est allé trop loin et avons dépassé la valeur cible,
                # on diminue le pas comme dans une dichotomie
                step = step / 2
            lastArea = self.area()
            if lastArea - area < 0 :
                for i in range(2, self.N) :
                    self.moveFreely(i, right, step)
            else :
                for i in range(2, self.N) :
                    self.moveFreely(i, left, step)



def list2poly(listeCoord) :
    vertices = ()
    for point in listeCoord :
        vertices += (Vertex(point[0], point[1]),)
    return Polygon(*vertices)
