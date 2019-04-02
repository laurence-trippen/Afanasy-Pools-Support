# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 02.04.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server Configurator - Main

import os
import sys
import cgruutils

from Qt import QtCore, QtGui, QtWidgets
from config import Config

# MainWindow class
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setFixedSize(340, 125)
        self.initUI()
        self.load()
    
    # UI initialization
    def initUI(self):
        # Window Title
        self.setWindowTitle('Pool Server Configurator   CGRU %s' %
                            os.getenv('CGRU_VERSION', ''))
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))
        
        self.ipLabel = QtWidgets.QLabel("Binding IP:")
        self.ipLineEdit = QtGui.QLineEdit()
        self.ipLineEdit.setPlaceholderText("If empty localhost is set.")
        self.ipLayout = QtWidgets.QHBoxLayout()
        self.ipLayout.addWidget(self.ipLabel)
        self.ipLayout.addWidget(self.ipLineEdit)

        self.portLabel = QtWidgets.QLabel("Port:")
        self.portSpinBox = QtGui.QSpinBox()
        self.portSpinBox.setMinimum(0)
        self.portSpinBox.setMaximum(65535)
        self.portLayout = QtWidgets.QHBoxLayout()
        self.portLayout.addWidget(self.portLabel)
        self.portLayout.addWidget(self.portSpinBox)

        self.maxClientsLabel = QtWidgets.QLabel("Max. Clients: (Renderfarm clients.)")
        self.maxClientsSpinBox = QtGui.QSpinBox()
        self.maxClientsSpinBox.setMinimum(0)
        self.maxClientsSpinBox.setMaximum(100000)
        self.maxClientsLayout = QtWidgets.QHBoxLayout()
        self.maxClientsLayout.addWidget(self.maxClientsLabel)
        self.maxClientsLayout.addWidget(self.maxClientsSpinBox)

        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.clicked.connect(self.save)

        # Top Root Layout
        self.topLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout.addLayout(self.ipLayout)
        self.topLayout.addLayout(self.portLayout)
        self.topLayout.addLayout(self.maxClientsLayout)
        self.topLayout.addWidget(self.saveButton)
    
    # Loads config
    def load(self):
        Config.check()
        Config.load()
        self.ipLineEdit.setText(Config.ip)
        self.portSpinBox.setValue(Config.port)
        self.maxClientsSpinBox.setValue(Config.max_clients)

    # Saves config
    def save(self):
        Config.save({
            "ip":self.ipLineEdit.text(),
            "port":self.portSpinBox.value(),
            "max_clients":self.maxClientsSpinBox.value()
        })
        self.close()

if __name__ == "__main__":
    if "CGRU_LOCATION" in os.environ:
        print("CGRU_LOCATION=" + os.environ['CGRU_LOCATION'])
    else:
        print("CGRU_LOCATION is not set!")
        sys.exit()
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())