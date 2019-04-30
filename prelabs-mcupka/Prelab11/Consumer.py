
#######################################################
#   Author:     Michael Cupka
#   email:      mcupka@purdue.edu
#   ID:         ee364d22
#   Date:       3/31/19
#######################################################

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from BasicUI import *
import re


class Consumer(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Consumer, self).__init__(parent)
        self.setupUi(self)
        self.btnClear.clicked.connect(self.Clear)
        self.txtBoxes = [self.txtComponentCount_1, self.txtComponentCount_2, self.txtComponentCount_3, self.txtComponentCount_4, self.txtComponentCount_5, self.txtComponentCount_6, self.txtComponentCount_7, self.txtComponentCount_8, self.txtComponentCount_9, self.txtComponentCount_10, self.txtComponentCount_11, self.txtComponentCount_12, self.txtComponentCount_13, self.txtComponentCount_14, self.txtComponentCount_15, self.txtComponentCount_16, self.txtComponentCount_17, self.txtComponentCount_18, self.txtComponentCount_19, self.txtComponentCount_20, self.txtComponentName_1, self.txtComponentName_2, self.txtComponentName_3, self.txtComponentName_4, self.txtComponentName_5, self.txtComponentName_6, self.txtComponentName_7, self.txtComponentName_8, self.txtComponentName_9, self.txtComponentName_10, self.txtComponentName_11, self.txtComponentName_12, self.txtComponentName_13, self.txtComponentName_14, self.txtComponentName_15, self.txtComponentName_16, self.txtComponentName_17, self.txtComponentName_18, self.txtComponentName_19, self.txtComponentName_20, self.txtStudentName, self.txtStudentID]
        self.Clear()
        self.dataPairs = [(self.txtComponentName_1, self.txtComponentCount_1), (self.txtComponentName_2, self.txtComponentCount_2), (self.txtComponentName_3, self.txtComponentCount_3), (self.txtComponentName_4, self.txtComponentCount_4), (self.txtComponentName_5, self.txtComponentCount_5), (self.txtComponentName_6, self.txtComponentCount_6), (self.txtComponentName_7, self.txtComponentCount_7), (self.txtComponentName_8, self.txtComponentCount_8), (self.txtComponentName_9, self.txtComponentCount_9), (self.txtComponentName_10, self.txtComponentCount_10), (self.txtComponentName_11, self.txtComponentCount_11), (self.txtComponentName_12, self.txtComponentCount_12), (self.txtComponentName_13, self.txtComponentCount_13), (self.txtComponentName_14, self.txtComponentCount_14), (self.txtComponentName_15, self.txtComponentCount_15), (self.txtComponentName_16, self.txtComponentCount_16), (self.txtComponentName_17, self.txtComponentCount_17), (self.txtComponentName_18, self.txtComponentCount_18), (self.txtComponentName_19, self.txtComponentCount_19), (self.txtComponentName_20, self.txtComponentCount_20)]

        for box in self.txtBoxes:
            box.textEdited.connect(self.DataModified)
        self.chkGraduate.stateChanged.connect(self.DataModified)
        self.cboCollege.currentIndexChanged.connect(self.DataModified)
        self.btnLoad.clicked.connect(self.loadData)
        self.btnSave.clicked.connect(self.saveData)

    def loadData(self):
        """
        *** DO NOT MODIFY THIS METHOD! ***
        Obtain a file name from a file dialog, and pass it on to the loading method. This is to facilitate automated
        testing. Invoke this method when clicking on the 'load' button.

        You must modify the method below.
        """
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open XML file ...', filter="XML files (*.xml)")

        if not filePath:
            return

        self.loadDataFromFile(filePath)

    def loadDataFromFile(self, filePath):
        """
        Handles the loading of the data from the given file name. This method will be invoked by the 'loadData' method.
        
        *** YOU MUST USE THIS METHOD TO LOAD DATA FILES. ***
        *** This method is required for unit tests! ***
        """
        in_file = open(filePath, 'r')

        xml_text = in_file.read()
        re_pattern = '\s<StudentName graduate="(.*)">(.*)</StudentName>'

        search = re.search(re_pattern, xml_text)

        self.txtStudentName.setText(search.group(2))
        self.chkGraduate.setCheckState(int(search.group(1)))

        re_pattern = '<StudentID>(.*)</StudentID>'
        search = re.search(re_pattern, xml_text)
        self.txtStudentID.setText(search.group(1))


        re_pattern = '<College>(.*)</College>'
        search = re.search(re_pattern, xml_text)
        self.cboCollege.setCurrentIndex(int(search.group(1)))

        re_pattern = '<Component name="(.*)" count="(.*)" />'
        search = re.findall(re_pattern, xml_text)

        for i in range(20):
            if i != None and i < len(search):
                namebox, countbox = self.dataPairs[i]
                name, count = search[i]
                namebox.setText(name)
                countbox.setText(count)


    def Clear(self):
        for box in self.txtBoxes:
            box.clear()
        self.chkGraduate.setCheckState(False)
        self.cboCollege.setCurrentIndex(0)
        self.btnSave.setEnabled(False)
        self.btnLoad.setEnabled(True)

    def DataModified(self):
        self.btnSave.setEnabled(True)
        self.btnLoad.setEnabled(False)

    def saveData(self):
        out_file = open("target.xml", 'w')
        xml_text = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                    + '<Content>\n' \
                    + f'\t<StudentName graduate="{self.chkGraduate.checkState()}">{self.txtStudentName.text()}</StudentName>\n' \
                    + f'\t<StudentID>{self.txtStudentID.text()}</StudentID>\n' \
                    + f'\t<College>{self.cboCollege.currentIndex()}</College>\n' \
                    + '\t<Components>\n'

        for name, count in self.dataPairs:
            xml_text += f'\t\t<Component name="{name.text()}" count="{count.text()}" />\n'


        xml_text += "\t</Components>\n"
        xml_text += "</Content>"
        out_file.write(xml_text)
        out_file.close()


if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Consumer()

    currentForm.show()
    currentApp.exec_()
