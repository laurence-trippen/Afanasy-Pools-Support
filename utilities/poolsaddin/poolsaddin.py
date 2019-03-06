# UTF-8

import os
import sys

from Qt import QtCore, QtGui, QtWidgets

import cgruutils

# MainWindow class
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        
        # Window Title
        self.setWindowTitle('Afanasy Pool Manager   CGRU %s' %
                            os.getenv('CGRU_VERSION', ''))
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon( QtGui.QIcon(iconpath))

        # Top Root Layout
        topLayout = QtWidgets.QVBoxLayout(self)

        poolsList = QtWidgets.QListWidget()
        poolsList.addItem("Test")

        topLayout.addWidget(poolsList)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())