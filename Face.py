from Point import *

class Face():
    def __init__(self, p1, p2, p3):
        ''' p1, p2, p3 are Points, this face has to be a triangle'''
        self.points = [p1, p2, p3]

    def area(self):
        ''' area of the triangle'''
        a = Point.distance(self.points[0], self.points[1])
        b = Point.distance(self.points[1], self.points[2])
        c = Point.distance(self.points[2], self.points[0])
        p = (a + b + c) / 2.
        return sqrt(p * (p - a) * (p - b) * (p - c))