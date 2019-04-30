#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        4/14/19
#######################################################

import numpy as np
import scipy.spatial
import scipy.interpolate
import re
import imageio
from PIL import Image
from MorphingApp import *


#function to load points and create triangles from the data
def loadTriangles(leftPointFilePath, rightPointFilePath):
    leftFile = open(leftPointFilePath, 'r')
    rightFile = open(rightPointFilePath, 'r')
    leftLines = leftFile.read().split('\n')
    rightLines = rightFile.read().split('\n')

    pointList = []
    leftTriangles = []
    for line in leftLines:
        mat = re.search(r'(\d+\.\d+)\s+(\d+\.\d+)', line)
        if mat != None:
            y = np.float64(mat.group(1))
            x = np.float64(mat.group(2))
            pointList.append((x, y))
    left_point_arr = np.array(pointList, dtype=np.float64)
    leftDel = scipy.spatial.Delaunay(left_point_arr)
    for verts in left_point_arr[leftDel.simplices]:
        tri = Triangle(verts)
        leftTriangles.append(tri)

    pointList = []
    rightTriangles = []
    for line in rightLines:
        mat = re.search(r'(\d+\.\d+)\s+(\d+\.\d+)', line)
        if mat != None:
            y = np.float64(mat.group(1))
            x = np.float64(mat.group(2))
            pointList.append((x, y))
    right_point_arr = np.array(pointList, dtype=np.float64)

    #use left triangles to get right ones, not delaunay
    for verts in right_point_arr[leftDel.simplices]:
        tri = Triangle(verts)
        rightTriangles.append(tri)

    return leftTriangles, rightTriangles


class Triangle:

    #init function
    def __init__(self, vertices):
        if vertices.shape != (3,2):
            raise ValueError('Must be 3x2 array')
        if vertices.dtype != np.float64:
            raise ValueError('Must be arr of type float64')
        self.vertices = vertices

    #get integer-valued points inside the triangle
    def getPoints(self):
        pointList = []

        v1 = self.vertices[0]
        v2 = self.vertices[1]
        v3 = self.vertices[2]

        x_max = self.vertices.max(0)[0]
        y_max = self.vertices.max(0)[1]
        x_min = self.vertices.min(0)[0]
        y_min = self.vertices.min(0)[1]

        # check all points in the rectangle to see if they are within the triangle
        xmin_floor = np.int(x_min)
        xmax_floor = np.int(x_max)
        ymin_floor = np.int(y_min)
        ymax_floor = np.int(y_max)

        x = xmin_floor
        while x <= xmax_floor:
            y = ymin_floor
            while y <= ymax_floor:
                if self.isPointInside(x, y): pointList.append((np.float64(x), np.float64(y)))
                y += np.uint8(1)
            x += np.uint8(1)

        point_arr = np.array(pointList, dtype=np.float64)
        return point_arr

    def isPointInside(self, x, y):
        v1 = self.vertices[0]
        v2 = self.vertices[1]
        v3 = self.vertices[2]
        x = np.float64(x)
        y = np.float64(y)

        a = (x - v2[0]) * (v1[1] - v2[1]) - (v1[0] - v2[0]) * (y - v2[1])
        b = (x - v3[0]) * (v2[1] - v3[1]) - (v2[0] - v3[0]) * (y - v3[1])
        c = (x - v1[0]) * (v3[1] - v1[1]) - (v3[0] - v1[0]) * (y - v1[1])

        return not ((a < 0) or (b < 0) or (c < 0)) and ((a > 0) or (b > 0) or (c > 0))


class Morpher:

    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        if not isinstance(leftImage, np.ndarray):
            raise TypeError('must be ndarrays')
        if not isinstance(rightImage, np.ndarray):
            raise TypeError('must be ndarrays')
        if leftImage.dtype != np.uint8:
            raise TypeError('images must be arr of type uint8')
        if rightImage.dtype != np.uint8:
            raise TypeError('images must be arr of type uint8')
        if not isinstance(leftTriangles, list) or not isinstance(leftTriangles[0], Triangle):
            raise TypeError('Triangles must be lists of Triangles')
        if not isinstance(rightTriangles, list) or not isinstance(leftTriangles[0], Triangle):
            raise TypeError('Triangles must be lists')

        self.leftImage = leftImage
        self.leftTriangles = leftTriangles
        self.rightImage = rightImage
        self.rightTriangles = rightTriangles

    def getImageAtAlpha(self, alpha):

        #canvas image
        final_image = np.zeros(shape=(self.leftImage.shape), dtype=np.uint8)

        #interpolations of both images so that we can access values at decimal indecies
        a = np.arange(np.shape(self.rightImage)[0])
        b = np.arange(np.shape(self.rightImage)[1])

        rightInt = scipy.interpolate.RectBivariateSpline(a, b, self.rightImage)
        leftInt = scipy.interpolate.RectBivariateSpline(a, b, self.leftImage)

        #steps:
        #for each triangle in source:
        #   1. get target triangle from l and r triangles and alpha
        #   2. get transform left onto target
        #   3. transform right onto target
        #   4. use alpha blending get final point values



        for i in range(len(self.leftTriangles)):
            #target tri
            middleTri = Triangle(np.float64(1.0 - alpha) * self.leftTriangles[i].vertices + np.float64(alpha) * self.rightTriangles[i].vertices)
            # transform left onto target

            b = np.array([[middleTri.vertices[0][0], middleTri.vertices[0][1], middleTri.vertices[1][0], middleTri.vertices[1][1], middleTri.vertices[2][0], middleTri.vertices[2][1]]]).T
            A = np.array([[self.leftTriangles[i].vertices[0][0], self.leftTriangles[i].vertices[0][1], 1, 0, 0, 0],[0, 0, 0, self.leftTriangles[i].vertices[0][0], self.leftTriangles[i].vertices[0][1], 1], [self.leftTriangles[i].vertices[1][0], self.leftTriangles[i].vertices[1][1], 1, 0, 0, 0],[0, 0, 0, self.leftTriangles[i].vertices[1][0], self.leftTriangles[i].vertices[1][1], 1], [self.leftTriangles[i].vertices[2][0], self.leftTriangles[i].vertices[2][1], 1, 0, 0, 0],[0, 0, 0, self.leftTriangles[i].vertices[2][0], self.leftTriangles[i].vertices[2][1], 1]])
            h = np.linalg.solve(A, b)
            H = np.array([[h[0][0], h[1][0], h[2][0]], [h[3][0], h[4][0], h[5][0]], [0, 0, 1]])
            Hinv = np.linalg.inv(H)

            #apply transformation to canvas
            for point in middleTri.getPoints():
                rSide = np.array([[point[0]], [point[1]], [1]])
                sol = np.matmul(Hinv, rSide)
                getx = int(sol[0][0])
                gety = int(sol[1][0])
                lval = leftInt(gety, getx)
                final_image[int(point[1])][int(point[0])] += np.int(np.round(np.float64(lval) *(1.0 - alpha)))


            #transform right onto target


            b = np.array([[middleTri.vertices[0][0], middleTri.vertices[0][1], middleTri.vertices[1][0], middleTri.vertices[1][1], middleTri.vertices[2][0], middleTri.vertices[2][1]]]).T
            A = np.array([[self.rightTriangles[i].vertices[0][0], self.rightTriangles[i].vertices[0][1], 1, 0, 0, 0],[0, 0, 0, self.rightTriangles[i].vertices[0][0], self.rightTriangles[i].vertices[0][1], 1], [self.rightTriangles[i].vertices[1][0], self.rightTriangles[i].vertices[1][1], 1, 0, 0, 0],[0, 0, 0, self.rightTriangles[i].vertices[1][0], self.rightTriangles[i].vertices[1][1], 1], [self.rightTriangles[i].vertices[2][0], self.rightTriangles[i].vertices[2][1], 1, 0, 0, 0],[0, 0, 0, self.rightTriangles[i].vertices[2][0], self.rightTriangles[i].vertices[2][1], 1]])
            h = np.linalg.solve(A, b)
            H = np.array([[h[0][0], h[1][0], h[2][0]], [h[3][0], h[4][0], h[5][0]], [0, 0, 1]])
            Hinv = np.linalg.inv(H)

            #apply transformation to canvas
            for point in middleTri.getPoints():
                rSide = np.array([[point[0]], [point[1]], [1]])
                sol = np.matmul(Hinv, rSide)
                getx = int(sol[0][0])
                gety = int(sol[1][0])
                rval = rightInt(gety, getx)
                final_image[int(point[1])][int(point[0])] += np.int(np.round(np.float64(rval) * alpha))

        return final_image




if __name__ == '__main__':
    verts = np.array(((0.0,0.0), (5.0,5.0), (5.0, 0.0)), dtype=np.float64)
    tri = Triangle(verts)
    points_in = tri.getPoints()
    leftTris, rightTris = loadTriangles('TestData/points.left.txt', 'TestData/points.right.txt')
    rimage = imageio.imread('TestData/RightGray.png')
    limage = imageio.imread('TestData/LeftGray.png')
    morph = Morpher(limage, leftTris, rimage, rightTris)
    final = morph.getImageAtAlpha(.25)
    finalio = Image.fromarray(final)
    finalio.show()
