#######################################################
#    Author:      Michael Cupka
#    email:       mcupka@purdue.edu
#    ID:          ee364d22
#    Date:        4/18/19
#######################################################

import sys
from MorphingGUI import *
from Morphing import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re
import numpy as np
import imageio
from PIL import ImageQt, Image

class MorphingApp(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)

        #disable some widgets
        self.alphaSlider.setEnabled(False)
        self.alphaBox.setEnabled(False)
        self.blendButton.setEnabled(False)

        #set default value for the alpha text box
        self.alphaBox.setText('0.5')

        #these are variables about the images loaded
        self.leftLoaded = False
        self.rightLoaded = False
        self.leftPoints = []
        self.rightPoints = []
        self.leftImagePath = ''
        self.rightImagePath = ''
        self.leftPointsPath = ''
        self.rightPointsPath = ''
        self.leftScene = QGraphicsScene()
        self.rightScene = QGraphicsScene()
        self.blendScene = QGraphicsScene()
        self.leftTriangles = []
        self.rightTriangles = []
        self.pointsPriorLeft = 0
        self.pointsPriorRight = 0
        self.pointsPersistedLeft = 0
        self.pointsPersistedRight = 0
        self.pointsUnpersistedLeft = 0
        self.pointsUnpersistedRight = 0
        self.newLeftSelected = False
        self.newRightSelected = False
        self.blendImage = QImage()

        #alpha value
        self.alphaValue = .5

        #connect the widgets to their corresponding functions
        self.startButton.clicked.connect(self.startLoad)
        self.endButton.clicked.connect(self.endLoad)
        self.triangleCheck.stateChanged.connect(self.showTriangles)
        self.startView.mousePressEvent = self.leftClicked
        self.endView.mousePressEvent = self.rightClicked
        self.mousePressEvent = self.formClicked
        self.keyPressEvent = self.keyPressed
        self.alphaSlider.valueChanged.connect(self.sliderChange)
        self.blendButton.pressed.connect(self.blend)

    def blend(self):
        #if there is an unpersisted point then persist it before blending
        if (self.newLeftSelected) and (self.newRightSelected):
            self.persistPoint()

        # we can only blend with triangles and we can only get triangles with at least 4 point pairs
        if len(self.leftTriangles) > 0 and len(self.rightTriangles) > 0:
            morph = Morpher(self.getNpImage(self.leftImagePath), self.leftTriangles, self.getNpImage(self.rightImagePath), self.rightTriangles)
            blend_arr = morph.getImageAtAlpha(self.alphaValue)
            image = self.npToImage(blend_arr)
            w, h = image.size().width(), image.size().height()
            pixmap = QPixmap()
            pixmap.convertFromImage(image)
            self.blendScene.clear()
            self.blendScene.addPixmap(pixmap)
            self.blendView.setScene(self.blendScene)
            self.blendView.fitInView(QGraphicsScene.itemsBoundingRect(self.blendScene), Qt.KeepAspectRatio)
            self.blendView.update()


    def sliderChange(self):
        #update the alpha value
        self.alphaValue = round(float(self.alphaSlider.value()) / 100.0, 2)
        self.alphaBox.setText('{:.2f}'.format(self.alphaValue))

    def formClicked(self, event):
        #this should only do something if both points are selected
        if (not self.newLeftSelected) or (not self.newRightSelected): return
        self.persistPoint()

    def persistPoint(self):
        #this function adds the currently selected points to the files and allows for another selection
        leftFile = open(self.leftPointsPath, 'w')
        rightFile = open(self.rightPointsPath, 'w')

        lines = []
        for p in self.leftPoints[0:-1]:
            lines.append('{:>8.1f}{:>8.1f}\n'.format(p[0], p[1]))
        lines.append('{:>8.1f}{:>8.1f}'.format(self.leftPoints[-1][0],self.leftPoints[-1][1]))
        leftFile.writelines(lines)

        lines = []
        for p in self.rightPoints[0:-1]:
            lines.append('{:>8.1f}{:>8.1f}\n'.format(p[0], p[1]))
        lines.append('{:>8.1f}{:>8.1f}'.format(self.rightPoints[-1][0],self.rightPoints[-1][1]))
        rightFile.writelines(lines)

        leftFile.close()
        rightFile.close()

        #reset the 'New Point Selected' values
        self.newRightSelected = False
        self.newLeftSelected = False
        self.pointsUnpersistedLeft -= 1
        self.pointsUnpersistedRight -= 1
        self.pointsPersistedLeft += 1
        self.pointsPersistedRight += 1
        self.genTriangles()
        self.refreshImages()


    def leftClicked(self, event):
        #This should only do something when both images are loaded
        if ((not self.rightLoaded) or (not self.leftLoaded)): return
        #It should also do nothing if the left point is selected already and the right is not
        if (self.newLeftSelected and (not self.newRightSelected)): return
        #if both points are selected, it should persist the pair befor selecting a new point
        if (self.newLeftSelected and self.newRightSelected):
            self.persistPoint()

        #If both images are loaded and no point is selected, get the point and add it to the points list
        x, y = (self.startView.mapToScene(event.pos()).x(), self.startView.mapToScene(event.pos()).y())
        max_x, max_y = (self.startView.scene().width(), self.startView.scene().height())

        #if the point selected is out of the bounds of the scene, do nothing
        if (x < 0.0 or x > max_x or y < 0 or y > max_y): return

        #append the point to the points list and increment the unpersisted variable so it appears green
        self.leftPoints.append((round(x, 1), round(y, 1)))
        self.pointsUnpersistedLeft += 1
        self.refreshImages()
        self.newLeftSelected = True

    def rightClicked(self, event):
        #This should only do something when both images are loaded
        if ((not self.rightLoaded) or (not self.leftLoaded)): return
        #It should also do nothing if the left point is not selected already or the right one is
        if ((not self.newLeftSelected) or self.newRightSelected): return

        # get point position and check it is within the bounds
        x, y = (self.endView.mapToScene(event.pos()).x(), self.endView.mapToScene(event.pos()).y())
        max_x, max_y = (self.endView.scene().width(), self.endView.scene().height())

        if (x < 0.0 or x > max_x or y < 0 or y > max_y): return

        #append the point to the points list and increment the unpersisted variable so it appears green
        self.rightPoints.append((round(x, 1), round(y, 1)))
        self.pointsUnpersistedRight += 1
        self.refreshImages()
        self.newRightSelected = True

    def keyPressed(self, event):
        if (event.key() == Qt.Key_Backspace):
            #this should backspace the selected points
            if (self.newRightSelected):
                self.rightPoints = self.rightPoints[:-1] #remove right point
                self.newRightSelected = False
                self.pointsUnpersistedRight -= 1
            elif (self.newLeftSelected):
                self.leftPoints = self.leftPoints[:-1] #remove right point
                self.newLeftSelected = False
                self.pointsUnpersistedLeft -= 1
            self.refreshImages()

    def showTriangles(self):
       self.refreshImages()

    def startLoad(self):
        #open file dialog box to get the starting image file
        path, _ = QFileDialog.getOpenFileName()
        if path:
            self.leftImagePath = path
            self.drawImageLeft()

            #now load point files if there is one
            self.leftPointsPath = self.leftImagePath + '.txt'
            self.leftPoints = self.getPoints(self.leftPointsPath)
            self.pointsPriorLeft = len(self.leftPoints)
            self.drawPointsLeft()

            #Enable Controls and Load Triangles if Both Images Have Been Loaded
            self.leftLoaded = True
            if (self.rightLoaded == True):
                self.alphaSlider.setEnabled(True)
                self.alphaBox.setEnabled(True)
                self.blendButton.setEnabled(True)
                self.genTriangles()
                self.refreshImages()

    def endLoad(self):
        #open file dialog box to get the ending image file
        path, _ = QFileDialog.getOpenFileName()
        if path:
            self.rightImagePath = path
            self.drawImageRight()

            #now load point files if there is one
            self.rightPointsPath = self.rightImagePath + '.txt'
            self.rightPoints = self.getPoints(self.rightPointsPath)
            self.pointsPriorRight = len(self.rightPoints)
            self.drawPointsRight()

            #Enable Controls and Load Triangles if Both Images Have Been Loaded
            self.rightLoaded = True
            if (self.leftLoaded == True):
                self.alphaSlider.setEnabled(True)
                self.alphaBox.setEnabled(True)
                self.blendButton.setEnabled(True)
                self.genTriangles()
                self.refreshImages()

    def refreshImages(self):
        #this function will be used to update all of the graphics if a change is made
        if self.leftLoaded:
            self.drawImageRight()
            self.drawPointsRight()
            if self.triangleCheck.isChecked(): self.drawTrianglesRight()

        if self.rightLoaded:
            self.drawImageLeft()
            self.drawPointsLeft()
            if self.triangleCheck.isChecked(): self.drawTrianglesLeft()


    def genTriangles(self):
        # We need at least 4 point pairs to do triangle calculations
        if (self.pointsPriorRight + self.pointsPersistedRight < 4): return
        if (self.pointsPriorLeft + self.pointsPersistedLeft < 4): return

        self.leftTriangles, self.rightTriangles = loadTriangles(self.leftPointsPath, self.rightPointsPath)

    def drawTrianglesLeft(self):
        for t in self.leftTriangles:
            v = t.vertices
            # add each of the 3 lines in the triangle separately
            self.leftScene.addLine(v[0][0], v[0][1], v[1][0], v[1][1], QPen(QBrush(Qt.darkMagenta), 2.0))
            self.leftScene.addLine(v[1][0], v[1][1], v[2][0], v[2][1], QPen(QBrush(Qt.darkMagenta), 2.0))
            self.leftScene.addLine(v[2][0], v[2][1], v[0][0], v[0][1], QPen(QBrush(Qt.darkMagenta), 2.0))

    def drawTrianglesRight(self):
        for t in self.rightTriangles:
            v = t.vertices
            # add each of the 3 lines in the triangle separately
            self.rightScene.addLine(v[0][0], v[0][1], v[1][0], v[1][1], QPen(QBrush(Qt.darkMagenta), 2.0))
            self.rightScene.addLine(v[1][0], v[1][1], v[2][0], v[2][1], QPen(QBrush(Qt.darkMagenta), 2.0))
            self.rightScene.addLine(v[2][0], v[2][1], v[0][0], v[0][1], QPen(QBrush(Qt.darkMagenta), 2.0))

    def getPoints(self, filename) -> list:
        points = []
        try:
            pfile = open(filename)
            data = pfile.read().split('\n')
            for line in data:
                mat = re.search(r'(\d+\.\d+)\s+(\d+\.\d+)', line)
                if mat != None:
                    x = float(mat.group(1))
                    y = float(mat.group(2))
                    points.append((x, y))
            pfile.close()
        except FileNotFoundError:
            pass
        return points

    def drawPointsRight(self):
        brush = QBrush()
        for p in self.rightPoints[0:self.pointsPriorRight]:
            self.rightScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.red))
        for p in self.rightPoints[self.pointsPriorRight:self.pointsPriorRight + self.pointsPersistedRight]:
            self.rightScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.blue))
        for p in self.rightPoints[self.pointsPriorRight + self.pointsPersistedRight:len(self.rightPoints)]:
            self.rightScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.green))

        self.endView.setScene(self.rightScene)
        self.endView.update()

    def drawPointsLeft(self):
        brush = QBrush()
        for p in self.leftPoints[0:self.pointsPriorLeft]:
            self.leftScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.red))
        for p in self.leftPoints[self.pointsPriorLeft:self.pointsPriorLeft + self.pointsPersistedLeft]:
            self.leftScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.blue))
        for p in self.leftPoints[self.pointsPriorLeft + self.pointsPersistedLeft:len(self.leftPoints)]:
            self.leftScene.addEllipse(QRectF(p[0] - 10, p[1] - 10, 20, 20), brush=QBrush(Qt.green))

        self.startView.setScene(self.leftScene)
        self.startView.update()

    def drawImageLeft(self):
        image = QImage()
        image.load(self.leftImagePath)
        w, h = image.size().width(), image.size().height()
        pixmap = QPixmap(self.leftImagePath)
        self.leftScene.clear()
        self.leftScene.addPixmap(pixmap)
        self.startView.setScene(self.leftScene)
        self.startView.fitInView(QGraphicsScene.itemsBoundingRect(self.leftScene), Qt.KeepAspectRatio)
        self.startView.update()

    def drawImageRight(self):
        image = QImage()
        image.load(self.rightImagePath)
        w, h = image.size().width(), image.size().height()
        pixmap = QPixmap(self.rightImagePath)
        self.rightScene.clear()
        self.rightScene.addPixmap(pixmap)
        self.endView.setScene(self.rightScene)
        self.endView.fitInView(QGraphicsScene.itemsBoundingRect(self.rightScene), Qt.KeepAspectRatio)
        self.endView.update()

    #helper function to convert a numpy arr to image for display after the blending
    def npToImage(self, arr):
        im = Image.fromarray(arr)
        image = ImageQt.ImageQt(im)
        return image

    #helper function to get image as np array for sending to the blending algorithm
    def getNpImage(self, path):
        im = imageio.imread(path)
        return np.asarray(im)

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()
