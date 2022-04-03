# ref to https://www.saltycrane.com/blog/2007/12/pyqt-example-how-to-run-command-and/
import os
import sys
from PyQt5 import QtWidgets
import subprocess


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


class MyWindow(QtWidgets.QWidget):
    def __init__(self, *args):
        QtWidgets.QWidget.__init__(self, *args)

        # create objects
        label = QtWidgets.QLabel(self.tr("Enter command and press Return"))
        self.le = QtWidgets.QLineEdit()
        self.te = QtWidgets.QTextEdit()

        # layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.le)
        layout.addWidget(self.te)
        self.setLayout(layout)

        # create connection
        self.le.returnPressed.connect(self.run_command)

    def run_command(self):
        cmd = str(self.le.text())
        # result = subprocess.run([cmd], stdout=subprocess.PIPE)
        result = subprocess.getoutput("python3 code_generator_SVM_paper.py")
        # print(result)
        self.te.setText(result)
        # .stdout.decode('utf-8')

if __name__ == "__main__":
    main()
