# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calculator.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 185)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.edtNumber1 = QtWidgets.QLineEdit(self.centralwidget)
        self.edtNumber1.setGeometry(QtCore.QRect(70, 50, 146, 27))
        self.edtNumber1.setObjectName("edtNumber1")
        self.edtNumber2 = QtWidgets.QLineEdit(self.centralwidget)
        self.edtNumber2.setGeometry(QtCore.QRect(360, 50, 146, 27))
        self.edtNumber2.setObjectName("edtNumber2")
        self.lblNumber1 = QtWidgets.QLabel(self.centralwidget)
        self.lblNumber1.setGeometry(QtCore.QRect(110, 30, 71, 17))
        self.lblNumber1.setObjectName("lblNumber1")
        self.lblNumber2 = QtWidgets.QLabel(self.centralwidget)
        self.lblNumber2.setGeometry(QtCore.QRect(400, 30, 71, 17))
        self.lblNumber2.setObjectName("lblNumber2")
        self.cboOperation = QtWidgets.QComboBox(self.centralwidget)
        self.cboOperation.setGeometry(QtCore.QRect(230, 50, 111, 27))
        self.cboOperation.setObjectName("cboOperation")
        self.cboOperation.addItem("")
        self.cboOperation.addItem("")
        self.cboOperation.addItem("")
        self.cboOperation.addItem("")
        self.edtResult = QtWidgets.QLineEdit(self.centralwidget)
        self.edtResult.setGeometry(QtCore.QRect(560, 50, 146, 27))
        self.edtResult.setReadOnly(True)
        self.edtResult.setObjectName("edtResult")
        self.lblResult = QtWidgets.QLabel(self.centralwidget)
        self.lblResult.setGeometry(QtCore.QRect(600, 30, 71, 17))
        self.lblResult.setAlignment(QtCore.Qt.AlignCenter)
        self.lblResult.setObjectName("lblResult")
        self.lblEquals = QtWidgets.QLabel(self.centralwidget)
        self.lblEquals.setGeometry(QtCore.QRect(520, 50, 21, 17))
        self.lblEquals.setObjectName("lblEquals")
        self.btnCalculate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalculate.setGeometry(QtCore.QRect(240, 100, 251, 27))
        self.btnCalculate.setObjectName("btnCalculate")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblNumber1.setText(_translate("MainWindow", "Number 1"))
        self.lblNumber2.setText(_translate("MainWindow", "Number 2"))
        self.cboOperation.setItemText(0, _translate("MainWindow", "+"))
        self.cboOperation.setItemText(1, _translate("MainWindow", "-"))
        self.cboOperation.setItemText(2, _translate("MainWindow", "*"))
        self.cboOperation.setItemText(3, _translate("MainWindow", "/"))
        self.lblResult.setText(_translate("MainWindow", "Result"))
        self.lblEquals.setText(_translate("MainWindow", "="))
        self.btnCalculate.setText(_translate("MainWindow", "Calculate"))

