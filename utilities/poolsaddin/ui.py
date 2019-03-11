# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - User Interface

import os
import cgruutils

from Qt import QtCore, QtGui, QtWidgets
from model import AF_API

# Create Pool Window / Modal Form
class CreatePoolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreatePoolDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Create Pool")

        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))

        self.setFixedSize(400, 60)
        self.setModal(True)

        self.poolNameLineEdit = QtWidgets.QLineEdit()
        self.poolNameLineEdit.setPlaceholderText("Pool name")

        self.createPoolButton = QtWidgets.QPushButton("Create Pool")

        self.topLayout = QtWidgets.QHBoxLayout(self)
        self.topLayout.addWidget(self.poolNameLineEdit)
        self.topLayout.addWidget(self.createPoolButton)

    def getPoolName(self):
        return self.poolNameLineEdit.text()
    
    def createPool(self):
        pass

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

        clients = AF_API.request_renderclients()
        for client in clients:
            self.clientsList.addItem(client.hostname)

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
    
    def showCreatePoolDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Create Pool', 'Pool Name')
        if ok:
            self.poolsList.addItem(str(text))