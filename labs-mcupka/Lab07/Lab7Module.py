#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        2/27/19
#######################################################
import sys
import os


class Rectangle:
    def __init__(self, llPoint:tuple, urPoint:tuple):
        if (llPoint[0] > urPoint[0]): raise ValueError('Lower left x > than upper right x')
        elif (llPoint[1] > urPoint[1]): raise ValueError('Lower left y > than upper right y')
        else:
            self.llPoint = llPoint
            self.urPoint = urPoint

    def isSquare(self):
        return (self.urPoint[0] - self.llPoint[0]) == (self.urPoint[1] - self.llPoint[1])

    def intersectsWith(self, rec):
        corner_points = []
        corner_points.append(rec.llPoint)
        corner_points.append(rec.urPoint)
        corner_points.append((rec.llPoint[0], rec.urPoint[1]))
        corner_points.append((rec.urPoint[0], rec.llPoint[1]))
        for point in corner_points:
            if (point[0] > self.llPoint[0]) & (point[0] < self.urPoint[0]) & (point[1] > self.llPoint[1]) & (point[1] < self.urPoint[1]):
                return True
        return False

    def __eq__(self, rec):
        if type(rec) != Rectangle: raise TypeError('Operand for equality must be of type \'Rectangle\'')
        my_area = abs((self.urPoint[0] - self.llPoint[0]) * (self.urPoint[1] - self.llPoint[1]))
        other_area = abs((rec.urPoint[0] - rec.llPoint[0]) * (rec.urPoint[1] - rec.llPoint[1]))
        return my_area == other_area

class Circle:
    def __init__(self, center: tuple, radius: float):
        if radius <= 0: raise ValueError('Radius must be greater than 0')
        self.center = center
        self.radius = radius

    def intersectsWith(self, other):
        if type(other) == Rectangle:
            corner_points = []
            corner_points.append(other.llPoint)
            corner_points.append(other.urPoint)
            corner_points.append((rec.llPoint[0], rec.urPoint[1]))
            corner_points.append((rec.urPoint[0], rec.llPoint[1]))

            if (self.center[0] > corner_points[0][0]) & (self.center[0] < corner_points[1][0]):
                # test for collision with top or bottom side
                if (abs(self.center[1] - corner_points[0][1]) < self.radius) or (abs(self.center[1] - corner_points[1][1]) < self.radius): return True

            if (self.center[1] > corner_points[0][1]) & (self.center[1] < corner_points[1][1]):
                # test for collision with left and right side
                if (abs(self.center[0] - corner_points[0][0]) < self.radius) or (abs(self.center[0] - corner_points[1][0]) < self.radius): return True

            # if the center lies on a corner, it definitely intersects
            for point in corner_points:
                if self.center == point: return True

            # no collision
            return False


        elif type(other) == Circle:
            rad2 = other.radius
            cent2 = other.center

            center_dist = pow(pow(self.center[0] - cent2[0], 2) + pow(self.center[1] - cent2[1], 2), .5)
            if (self.radius + rad2) > center_dist: return True
            else: return False
        else:
            raise TypeError('Type must be Rectangle or Circle')

if __name__ == '__main__':
    rec = Rectangle((5.0, 5.0) , (10.0, 10.0))
    print(rec.isSquare())
    rec2 = Rectangle((0.0, 0.0), (10.0, 10.0))
    print(rec.intersectsWith(rec2))
    print(rec == rec2)
    circ = Circle((0.0, 0.0), 3.0)
    print(circ.intersectsWith(rec2))
    circ2 = Circle((5.0, 5.0), 1.0)
    print(circ.intersectsWith(circ2))