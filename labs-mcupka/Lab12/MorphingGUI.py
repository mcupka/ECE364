# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 742)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.startView = QtWidgets.QGraphicsView(self.centralwidget)
        self.startView.setGeometry(QtCore.QRect(60, 50, 281, 221))
        self.startView.setObjectName("startView")
        self.endView = QtWidgets.QGraphicsView(self.centralwidget)
        self.endView.setGeometry(QtCore.QRect(510, 50, 281, 221))
        self.endView.setObjectName("endView")
        self.blendView = QtWidgets.QGraphicsView(self.centralwidget)
        self.blendView.setGeometry(QtCore.QRect(270, 430, 281, 221))
        self.blendView.setObjectName("blendView")
        self.alphaSlider = QtWidgets.QSlider(self.centralwidget)
        self.alphaSlider.setGeometry(QtCore.QRect(110, 380, 591, 20))
        self.alphaSlider.setMaximum(100)
        self.alphaSlider.setSingleStep(1)
        self.alphaSlider.setSliderPosition(50)
        self.alphaSlider.setOrientation(QtCore.Qt.Horizontal)
        self.alphaSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.alphaSlider.setTickInterval(10)
        self.alphaSlider.setObjectName("alphaSlider")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(60, 20, 161, 27))
        self.startButton.setObjectName("startButton")
        self.endButton = QtWidgets.QPushButton(self.centralwidget)
        self.endButton.setGeometry(QtCore.QRect(630, 20, 161, 27))
        self.endButton.setObjectName("endButton")
        self.blendButton = QtWidgets.QPushButton(self.centralwidget)
        self.blendButton.setGeometry(QtCore.QRect(360, 660, 101, 27))
        self.blendButton.setObjectName("blendButton")
        self.alphaBox = QtWidgets.QLineEdit(self.centralwidget)
        self.alphaBox.setGeometry(QtCore.QRect(720, 370, 61, 27))
        self.alphaBox.setAlignment(QtCore.Qt.AlignCenter)
        self.alphaBox.setReadOnly(True)
        self.alphaBox.setObjectName("alphaBox")
        self.triangleCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.triangleCheck.setGeometry(QtCore.QRect(370, 320, 121, 22))
        self.triangleCheck.setObjectName("triangleCheck")
        self.startlabel = QtWidgets.QLabel(self.centralwidget)
        self.startlabel.setGeometry(QtCore.QRect(140, 280, 101, 17))
        self.startlabel.setObjectName("startlabel")
        self.endlabel = QtWidgets.QLabel(self.centralwidget)
        self.endlabel.setGeometry(QtCore.QRect(610, 280, 91, 17))
        self.endlabel.setObjectName("endlabel")
        self.startlabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.startlabel_2.setGeometry(QtCore.QRect(110, 400, 31, 20))
        self.startlabel_2.setObjectName("startlabel_2")
        self.startlabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.startlabel_3.setGeometry(QtCore.QRect(680, 400, 21, 17))
        self.startlabel_3.setObjectName("startlabel_3")
        self.startlabel_4 = QtWidgets.QLabel(self.centralwidget)
        self.startlabel_4.setGeometry(QtCore.QRect(70, 380, 41, 20))
        self.startlabel_4.setObjectName("startlabel_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Morphing Application"))
        self.startButton.setText(_translate("MainWindow", "Load Starting Image ..."))
        self.endButton.setText(_translate("MainWindow", "Load Ending Image ..."))
        self.blendButton.setText(_translate("MainWindow", "Blend"))
        self.triangleCheck.setText(_translate("MainWindow", "Show Triangles"))
        self.startlabel.setText(_translate("MainWindow", "Starting Image"))
        self.endlabel.setText(_translate("MainWindow", "Ending Image"))
        self.startlabel_2.setText(_translate("MainWindow", "0.0"))
        self.startlabel_3.setText(_translate("MainWindow", "1.0"))
        self.startlabel_4.setText(_translate("MainWindow", "Alpha"))

