# UTF-8

import sys

from Qt import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QtWidget):
    def __init__(self):
        # Main Window
        QtWidgets.QtWidget.__init__(self)
        self.constructed = False
        self.evaluated = False
        self.output = ''
        self.setWindowTitle('Afanasy Pool Vendor Client')

app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec_()