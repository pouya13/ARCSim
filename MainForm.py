""""
Random Instruction Generator (ARCSim)

Written by Pouya Narimani (pouyanarimani.kh@gmail.com).

(c) Copyright SCL, All Rights Reserved. NO WARRANTY.

"""

# import math
import sys, os
from Cores import *
from Instructions import *
# import pickle
# import subprocess
# import copy
# from skimage import draw

# import matplotlib.pyplot as plt

from contextlib import contextmanager
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QApplication, QFileDialog, QLineEdit, QLabel

# from PySide2.QtGui import QFrame

from PyQt5.QtCore import Qt



# from PyQt5.QtGui import QPainter, QPen


class MainForm(QtWidgets.QMainWindow):
    dicom = None
    signal = QtCore.pyqtSignal()
    beginDistance = (0, 0, 0)
    endDistance = (0, 0, 0)

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.cores = Cores()
        self.initUI()

    def initUI(self):
        # Settings.init()  # Call only once

        self.setGeometry(0, 0, 1000, 500)
        self.setFixedSize(500, 600)
        self.setWindowTitle('ARCSim: Main') # AVR Random Code generator for Side channel attacks
        self.setMinimumSize(1000, 600)
        self.statusBar()

        # layoutGrid = QGridLayout()
        # self.setLayout(layoutGrid)

        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)

        self.Quality = False

        self.lastvalue = 0


        # vivi = QFrame()
        # vivi.setFrameShape(QtGui.QFrame.HLine)
        # vivi.setFrameShadow(QtGui.QFrame.Sunken)
        # layoutGrid.addWidget(vivi, 1, 0, 1, 2)

        path = os.getcwd()
        path = path.split('/')
        self.maindir = '/' + str(path[1]) + '/' + str(path[2])
        self.maindir = os.getcwd()

        self.FileCounter = 1


        # region code type
        self.Codetype = QtWidgets.QGroupBox('&Code Type', self)
        self.Codetype.move(50, 60)
        self.Codetype.resize(260, 80)

        # list
        self.Types = QtWidgets.QComboBox(self.Codetype)
        self.Types.addItem("Code Types")
        self.Types.addItem("Framed")
        self.Types.addItem("Raw")
        self.Types.move(10, 30)
        self.Types.resize(150, 30)


        # text box
        # self.textbox1 = QtWidgets.QLineEdit(self.Codetype, placeholderText="Ins. #")
        # self.textbox1.move(180,30)
        # self.textbox1.resize(70,30)

        # end region



        # region cores
        self.CoreSelection = QtWidgets.QGroupBox('&Core Selection', self)
        self.CoreSelection.move(50, 170)
        self.CoreSelection.resize(260, 80)

        # list
        self.Cores = QtWidgets.QComboBox(self.CoreSelection)
        self.Cores.addItem("Core Selection")
        for i in range(self.cores.get_len()):
            self.Cores.addItem(self.cores.get_cores()[i])
        self.Cores.move(10, 30)
        self.Cores.resize(150, 30)


        # text box
        self.textbox1 = QtWidgets.QLineEdit(self.CoreSelection, placeholderText="Ins. #")
        self.textbox1.move(180,30)
        self.textbox1.resize(70,30)

        # end region


        # region new code
        self.NewCode = QtWidgets.QGroupBox('&New Code', self)
        self.NewCode.move(50, 280)
        self.NewCode.resize(260, 80)
        
        # button
        self.openDir = QtWidgets.QPushButton("&New Code", self.NewCode)
        self.openDir.move(10, 35)
        self.openDir.resize(100, 30)
        self.openDir.clicked.connect(self.newcode)

        # text box
        self.textbox2 = QtWidgets.QLineEdit(self.NewCode, placeholderText="File # to start")
        self.textbox2.move(125,35)
        self.textbox2.resize(120,30)

        # end region


        # region compile and program
        self.CompileReg = QtWidgets.QGroupBox('&Compile', self)
        self.CompileReg.move(390, 170)
        self.CompileReg.resize(260, 80)

        # button
        self.Compile = QtWidgets.QPushButton("&Compile", self.CompileReg)
        self.Compile.move(10, 30)
        self.Compile.resize(100, 30)
        self.Compile.clicked.connect(self.compile)

        # button
        self.Program = QtWidgets.QPushButton("&Program", self.CompileReg)
        self.Program.move(140, 30)
        self.Program.resize(100, 30)
        self.Program.clicked.connect(self.program)

        # end region


        # region simulation
        self.Simulate = QtWidgets.QGroupBox('&Simulation', self)
        self.Simulate.move(390, 280)
        self.Simulate.resize(260, 80)

        # button
        self.simulate = QtWidgets.QPushButton("&Simulate", self.Simulate)
        self.simulate.move(10, 30)
        self.simulate.resize(100, 30)
        self.simulate.clicked.connect(self.simavr)

        # end region



        # region save
        self.Save = QtWidgets.QGroupBox('&Save', self)
        self.Save.move(230, 400)
        self.Save.resize(260, 80)

        # list
        self.TrainOrTest = QtWidgets.QComboBox(self.Save)
        self.TrainOrTest.addItem("Train or Test")
        self.TrainOrTest.addItem("Train")
        self.TrainOrTest.addItem("Test")
        self.TrainOrTest.move(10, 30)
        self.TrainOrTest.resize(120, 30)


        # button
        self.SaveFiles = QtWidgets.QPushButton("&Save", self.Save)
        self.SaveFiles.move(160, 30)
        self.SaveFiles.resize(80, 30)
        self.SaveFiles.clicked.connect(self.savefiles)

        # end region



        # region textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(50, 530)
        self.textbox.resize(600,50)
        self.textbox.setStyleSheet("color: white;  background-color: black")

        self.textboxLabel = QLabel(self)
        self.textboxLabel.setText('Message')
        self.textboxLabel.move(50, 505)

        # end region



        # image
        main_icon_label = QtWidgets.QLabel(self)
        main_icon = QtGui.QPixmap('Resource/AVR')
        main_icon_label.setPixmap(main_icon)
        main_icon_label.setScaledContents(True)
        main_icon_label.move(700, 300)
        main_icon_label.resize(250, 250)

        # image
        scl_icon_label = QtWidgets.QLabel(self)
        scl_icon = QtGui.QPixmap('Resource/SCL')
        scl_icon_label.setPixmap(scl_icon)
        scl_icon_label.setScaledContents(True)
        scl_icon_label.move(730, 50)
        scl_icon_label.resize(200, 200)



        openFile = QtWidgets.QAction('About', self)
        # openFile.setShortcut('Ctrl+O')
        # openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&About')
        fileMenu.addAction(openFile)


    def LoadDir(self):
        self.maindir = QtWidgets.QFileDialog.getExistingDirectory()


    def reset(self):
        os.system('c')

    def savefiles(self):
        if self.TrainOrTest.currentIndex() == 1:
            os.system("mkdir train_codes")
            os.system("mv my_labels" + str(self.FileCounter-1) + ".txt train_codes/")
            os.system("mv code" + str(self.FileCounter-1) + ".hex train_codes/")
            os.system("mv code" + str(self.FileCounter-1) + ".s train_codes/")
            self.textbox.setText("Code and labels were saved to \'train_codes\' directory.")
        elif self.TrainOrTest.currentIndex() == 2:
            os.system("mkdir test_codes")
            os.system("mv my_labels" + str(self.FileCounter-1) + ".txt test_codes/")
            os.system("mv code" + str(self.FileCounter-1) + ".hex test_codes/")
            os.system("mv code" + str(self.FileCounter-1) + ".s test_codes/")
            self.textbox.setText("Code and labels were saved to \'test_codes\' directory.")
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Please, select train or test type')
            msg.exec_()


    def newcode(self):
        if self.Types.currentIndex() == 1:
            if self.Cores.currentIndex() == 1:
                if self.textbox1.text():
                    newcode = Instructions(int(self.textbox1.text()), self.maindir)
                    newcode.set_instructions(self.cores.get_instruction_sets())
                    newcode.generate_new_framed_code(self.generate_filename())
                    del newcode
                    self.textbox.setText("New code generated.")
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setWindowTitle("Error")
                    msg.setText('Please, determine instruction numbers.')
                    msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Error")
                msg.setText('Please, determine the avr core.')
                msg.exec_()
        elif self.Types.currentIndex() == 2:
            if self.Cores.currentIndex() == 1:
                if self.textbox1.text():
                    newcode = Instructions(int(self.textbox1.text()), self.maindir)
                    newcode.set_instructions(self.cores.get_instruction_sets())
                    newcode.generate_new_raw_code(self.generate_filename())
                    del newcode
                    self.textbox.setText("New code generated.")
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setWindowTitle("Error")
                    msg.setText('Please, determine instruction numbers.')
                    msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Error")
                msg.setText('Please, determine the avr core.')
                msg.exec_()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Error")
            msg.setText('Please, determine the code type.')
            msg.exec_()

    
    def generate_filename(self):
        if self.textbox2.text():
            if self.lastvalue != int(self.textbox2.text()):
                self.lastvalue = int(self.textbox2.text())
                self.FileCounter = int(self.textbox2.text())

        FileName = '/code' + str(self.FileCounter) + '.s'
        self.FileCounter += 1
        return FileName

        
    def simavr(self):
        if self.Types.currentIndex() == 1:
            try:
                command = './simavr-master-v1/simavr/run_avr -m atmega8 -f 8000000 ' + 'code' + str(self.FileCounter-1) + '.hex'
                os.system(command)
                command = './clean_labels_v1.sh'
                os.system(command)
                command = 'mv my_labels.txt my_labels' + str(self.FileCounter-1) + '.txt'
                os.system(command)
                self.textbox.setText("Hex code simulated, and cleaned labels were saved to current directory.")
            except:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Error")
                msg.setText('Could not find "simavr-master" folder.')
                msg.exec_()
        elif self.Types.currentIndex() == 2:
            try:
                command = './simavr-master-v2/simavr/run_avr -m atmega8 -f 8000000 ' + 'code' + str(self.FileCounter-1) + '.hex'
                os.system(command)
                command = './clean_labels_v2.sh'
                os.system(command)
                command = 'mv my_labels.txt my_labels' + str(self.FileCounter-1) + '.txt'
                os.system(command)
                self.textbox.setText("Hex code simulated, and cleaned labels were saved to current directory.")
            except:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowTitle("Error")
                msg.setText('Could not find "simavr-master" folder.')
                msg.exec_()


    def compile(self):
        command = 'avr-gcc -xassembler-with-cpp ' + self.maindir + '/code' + str(self.FileCounter-1) + '.s -mmcu=atmega8 -nostdlib -o ' + self.maindir + '/a.out'
        os.system(command)
        command = 'avr-objcopy -j .text -j .data -O ihex ' + self.maindir + '/a.out ' + self.maindir + '/code' + str(self.FileCounter-1) + '.hex'
        os.system(command)
        command = 'rm -rf ' + self.maindir + '/a.out'
        os.system(command)
        self.textbox.setText("Your code compiled and the hex file was saved to current directory.")

    def program(self):
        sudoPassword = '1253'
        command = 'chmod a+rw /dev/ttyUSB0'
        os.system('echo %s|sudo -S %s' % (sudoPassword, command))
        # os.system('sudo chmod a+rw /dev/ttyUSB0')
        command = 'avrdude -c arduino -p atmega8 -P /dev/ttyUSB0 -b 19200 -U flash:w:' + self.maindir + '/code' + str(self.FileCounter-1) + '.hex'
        os.system(command)
        self.textbox.setText("Your code programmed to device.")


    @contextmanager
    def WaitCursor(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
            yield
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

        coreg = []


    def closeEvent(self, eventQCloseEvent):
        eventQCloseEvent.ignore()
        answer = QtWidgets.QMessageBox.question(
            self,
            'quit',
            'Are you sure you want to quit ?',
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)
        if (answer == QtWidgets.QMessageBox.Yes):
            QtCore.QCoreApplication.exit(0)
            # eventQCloseEvent.accept()
        else:
            eventQCloseEvent.ignore()


    def about(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("About")
        msg.setText('Wellcome to random instruction generator and simulator.\n'+'This is a tool for Side Channel Attacks. You can generate as many uniform random instructions. This tool exports a hex file, assembly file and labels file.\n'+
            'Any suggestions would be appreciated: pouyanarimani.kh@gmail.com')
        msg.exec_()