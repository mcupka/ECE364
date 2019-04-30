"""
Creating a PyQt Application:

1- Create a UI file using the QtDesigner.

2- Convert the UI file to a Python file using the conversion tool:
    /package/eda/anaconda3/bin/pyuic5 <fileName.ui> -o <fileName.py>
   The generated file must NOT be modified, as indicated in the header warning!
   
3- Use the given file <blank.py> to create a consumer Python file, and write the code that drives the UI.

"""

# Import PyQt5 classes
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication

from calculator import *

class MathConsumer(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MathConsumer, self).__init__(parent)
        self.setupUi(self)
        self.btnCalculate.clicked.connect(self.performOperation)


    def performOperation(self):
        # get two numbers from text boxes
        a = self.edtNumber1.text()
        b = self.edtNumber2.text()

        try:
            a = float(a)
            b = float(b)

            if self.cboOperation.currentText() == '+': res = a + b
            elif self.cboOperation.currentText() == '-': res = a - b
            elif self.cboOperation.currentText() == '*': res = a * b
            elif self.cboOperation.currentText() == '/': res = a / b

            self.edtResult.setText(str(res))

        except ValueError:
            self.edtResult.setText('E')

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MathConsumer()

    currentForm.show()
    currentApp.exec_()


