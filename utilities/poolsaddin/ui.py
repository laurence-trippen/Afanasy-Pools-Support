# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - User Interface

import os
import db
import cgruutils

from Qt import QtCore, QtGui, QtWidgets
from model import AF_API, AF_RenderPool

# MainWindow class
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    # UI Initialization
    def initUI(self):
        # Window Title
        self.setWindowTitle('Afanasy Pool Manager   CGRU %s' %
                            os.getenv('CGRU_VERSION', ''))
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))

        self.poolsLabel = QtWidgets.QLabel("Pools")

        self.poolsList = QtWidgets.QListWidget()

        self.createPoolButton = QtWidgets.QPushButton("Create")
        self.createPoolButton.clicked.connect(self.showCreatePoolDialog)

        self.deletePoolButton = QtWidgets.QPushButton("Delete")
        self.editPoolButton = QtWidgets.QPushButton("Edit")

        self.poolsButtonLayout = QtWidgets.QHBoxLayout()
        self.poolsButtonLayout.addWidget(self.createPoolButton)
        self.poolsButtonLayout.addWidget(self.editPoolButton)
        self.poolsButtonLayout.addWidget(self.deletePoolButton)

        self.poolsLayout = QtWidgets.QVBoxLayout()
        self.poolsLayout.addWidget(self.poolsLabel)
        self.poolsLayout.addWidget(self.poolsList)
        self.poolsLayout.addLayout(self.poolsButtonLayout)

        self.clientsLabel = QtWidgets.QLabel("Clients")
        
        self.clientsList = QtWidgets.QListWidget()

        self.addClientButton = QtWidgets.QPushButton("Add Client")
        self.removeClientButton = QtWidgets.QPushButton("Remove Client")

        self.clientsButtonLayout = QtWidgets.QHBoxLayout()
        self.clientsButtonLayout.addWidget(self.addClientButton)
        self.clientsButtonLayout.addWidget(self.removeClientButton)

        self.clientsLayout = QtWidgets.QVBoxLayout()
        self.clientsLayout.addWidget(self.clientsLabel)
        self.clientsLayout.addWidget(self.clientsList)
        self.clientsLayout.addLayout(self.clientsButtonLayout)

        self.listsLayout = QtWidgets.QHBoxLayout()
        self.listsLayout.addLayout(self.poolsLayout)
        self.listsLayout.addLayout(self.clientsLayout)

        # Top Root Layout
        self.topLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout.addLayout(self.listsLayout)

        # Inits the MenuBar
        self.initMenuBar()
        self.loadAndFillPools()

    def initMenuBar(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.menubar = QtGui.QMenuBar()

        self.fileMenu = self.menubar.addMenu('File')
        self.fileMenu.addAction(exitAction)

        self.settingsMenu = self.menubar.addMenu('Settings')

        self.topLayout.setMenuBar(self.menubar)

    def loadAndFillPools(self):
        pools = db.connection.findAllPools()
        for pool in pools:
            self.poolsList.addItem(pool.name)
    
    def showCreatePoolDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Create Pool', 'Pool Name')
        if ok and str(text) != "":
            result = db.connection.insertPool(AF_RenderPool(text))
            if result["acknowledged"]:
                self.poolsList.addItem(str(text))
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(str(result["e"]))
                msgBox.exec_()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("Pool name is empty!")
            msgBox.exec_()