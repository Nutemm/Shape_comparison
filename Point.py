from math import sqrt

class Point():

    def __init__(self, x, y, z, c):
        ''' x, y, z are the coords, c is the index in the list of vertices'''
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.index = c

    def distance(p1, p2):
        ''' euclidean distance between two points'''
        return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y) + (p1.z - p2.z) * (p1.z - p2.z))
