# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - User Interface

import os
import db
import cgruutils

from Qt import QtCore, QtGui, QtWidgets
from model import AF_API, AF_RenderPool, AF_RenderClient
from network import LANScanner

# MainWindow class
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.selected_pool = None
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
        self.poolsList.itemClicked.connect(self.onItemClicked)
        # self.poolsList.selectionModel().setCurrentIndex(self.poolsList.model().index(1,1), QtGui.QItemSelectionModel.SelectionFlag.Select)

        self.createPoolButton = QtWidgets.QPushButton("Create")
        self.createPoolButton.clicked.connect(self.showCreatePoolDialog)

        self.deletePoolButton = QtWidgets.QPushButton("Delete")
        self.deletePoolButton.clicked.connect(self.showDeletePoolDialog)

        self.editPoolButton = QtWidgets.QPushButton("Edit")
        self.editPoolButton.clicked.connect(self.showEditPoolDialog)

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

        self.addClientButton = QtWidgets.QPushButton("Add Client(s)")
        self.addClientButton.clicked.connect(self.showAddClientWindow)

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
        self.initStatusBar()
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
        self.helpMenu = self.menubar.addMenu('?')
        self.topLayout.setMenuBar(self.menubar)
    
    def initStatusBar(self):
        self.statusbar = QtGui.QStatusBar()
        self.statusbar.showMessage(db.MongoDBConnector.status)
        self.topLayout.addWidget(self.statusbar)

    def loadAndFillPools(self):
        self.pools = db.connection.findAllPools()
        for pool in self.pools:
            self.poolsList.addItem(pool.name)
    
    def showCreatePoolDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Create Pool', 'Pool Name')
        if ok and str(text) != "":
            pool = AF_RenderPool(text)
            pool.clients.append(AF_RenderClient("lt-pc-01", "", "", ""))
            pool.clients.append(AF_RenderClient("lt-pc-02", "", "", ""))
            result = db.connection.insertPool(pool)
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

    def showEditPoolDialog(self):
        currentItem = self.poolsList.currentItem()
        text, ok = QtGui.QInputDialog.getText(self, "New Pool Name", "New Pool Name", text=currentItem.text())
        if ok and str(text) != "":
            result = db.connection.updatePoolName(currentItem.text(), text)
            if result["acknowledged"]:
                currentItem.setText(text)
                self.poolsList.editItem(currentItem)
            else:
                msgBox = QtGui.QMessageBox()
                msgBox.setText(str(result["e"]))
                msgBox.exec_()

    def showDeletePoolDialog(self):
        currentItem = self.poolsList.currentItem()
        flags = QtGui.QMessageBox.StandardButton.Yes
        flags |= QtGui.QMessageBox.StandardButton.No
        question = "Do you realy want to delete the pool '" + currentItem.text() + "'?"
        response = QtGui.QMessageBox.question(self, "Question", question, flags)
        if response == QtGui.QMessageBox.Yes:
            result = db.connection.deletePool(currentItem.text())
            if result["acknowledged"]:
                self.poolsList.takeItem(self.poolsList.currentRow())

    def showAddClientWindow(self):
        if self.selected_pool != None:
            self.addClientWindow = AddClientWindow(self.selected_pool)
            self.addClientWindow.show()
        else:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("No pool selected!")
            msgBox.exec_()
    
    def onItemClicked(self, item):
        for pool in self.pools:
            if pool.name == item.text():
                self.selected_pool = pool
                self.clientsList.clear()
                for client in pool.clients:
                    self.clientsList.addItem(client.hostname)

class NetworkScanWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setFixedSize(340, 60)
        self.initUI()

        self.lanScannerThread = LANScanner()
        self.lanScannerThread.updateProgress.connect(self.setProgress)
        self.lanScannerThread.finished.connect(self.onFinished)
        self.lanScannerThread.terminated.connect(self.onTerminated)
        self.lanScannerThread.start()
    
    def initUI(self):
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Window Title
        self.setWindowTitle("Scanning network for hosts ...")
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))
        
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.minimum = 1
        self.progressBar.maximum = 100

        self.topLayout = QtWidgets.QHBoxLayout(self)
        self.topLayout.addWidget(self.progressBar)
    
    def setProgress(self, progress):
        self.progressBar.setValue(progress)

    def onFinished(self):
        self.close()
    
    def onTerminated(self):
        self.close()

class AddClientWindow(QtWidgets.QWidget):
    def __init__(self, selected_pool):
        QtWidgets.QWidget.__init__(self)
        self.initSelectedPool(selected_pool)
        self.initUI()
        self.loadAFClients()

    def initSelectedPool(self, selected_pool):
        self.selected_pool = selected_pool
        self.pool_hostnames = []
        for client in selected_pool.clients:
            self.pool_hostnames.append(client.hostname)

    # UI Initialization
    def initUI(self):
        self.setFixedSize(720, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Window Title
        self.setWindowTitle("Add Client(s)")
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))

        self.networkList = QtWidgets.QListWidget()
        self.scanNetworkButton = QtWidgets.QPushButton("Scan Network")
        self.scanNetworkButton.clicked.connect(self.scanNetwork)
        
        self.networkLayout = QtWidgets.QVBoxLayout()
        self.networkLayout.addWidget(self.networkList)
        self.networkLayout.addWidget(self.scanNetworkButton)

        self.networkGroupBox = QtWidgets.QGroupBox("Local Network")
        self.networkGroupBox.setLayout(self.networkLayout)

        self.addHostnameButton = QtWidgets.QPushButton("(+) Hostname")
        self.addHostnameButton.clicked.connect(self.addHostname)

        self.remHostnameButton = QtWidgets.QPushButton("(-) Hostname")
        self.remHostnameButton.clicked.connect(self.removeHostname)

        self.hostnamesButtonsLayout = QtWidgets.QHBoxLayout()
        self.hostnamesButtonsLayout.addWidget(self.addHostnameButton)
        self.hostnamesButtonsLayout.addWidget(self.remHostnameButton)

        self.hostnamesList = QtWidgets.QListWidget()
        self.hostnamesLayout = QtWidgets.QVBoxLayout()
        self.hostnamesLayout.addWidget(self.hostnamesList)
        self.hostnamesLayout.addLayout(self.hostnamesButtonsLayout)

        self.hostnamesGroupBox = QtWidgets.QGroupBox("Hostnames")
        self.hostnamesGroupBox.setLayout(self.hostnamesLayout)

        self.clientsList = QtWidgets.QListView()
        self.clientsModel = QtGui.QStandardItemModel(self.clientsList)
        self.clientsList.setModel(self.clientsModel)

        self.clientsLayout = QtWidgets.QVBoxLayout()
        self.clientsLayout.addWidget(self.clientsList)

        self.clientsGroupBox = QtWidgets.QGroupBox("Afanasy Clients")
        self.clientsGroupBox.setLayout(self.clientsLayout)
       
        self.groupBoxesLayout = QtWidgets.QHBoxLayout()
        self.groupBoxesLayout.addWidget(self.clientsGroupBox)
        self.groupBoxesLayout.addWidget(self.hostnamesGroupBox)
        self.groupBoxesLayout.addWidget(self.networkGroupBox)

        self.saveButton = QtWidgets.QPushButton("Save")

        self.topLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout.addLayout(self.groupBoxesLayout)
        self.topLayout.addWidget(self.saveButton)

    def loadAFClients(self):
        self.af_clients = AF_API.request_renderclients()
        for client in self.af_clients:
            if client in self.selected_pool.clients:
                print("IN")
                item = QtGui.QStandardItem(client.hostname + " (" + client.ip + ")")
                item.setCheckable(True)
                item.setEnabled(False)
                self.clientsModel.appendRow(item)
            else:
                print("NOT IN")
                item = QtGui.QStandardItem(client.hostname + " (" + client.ip + ")")
                item.setCheckable(True)
                self.clientsModel.appendRow(item)

    def addHostname(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Add Hostname', 'Hostname')
        if ok and str(text) != "":
            if text in self.pool_hostnames:
                msgBox = QtGui.QMessageBox()
                msgBox.setText("Hostname already exists!")
                msgBox.exec_()
            else:
                self.hostnamesList.addItem(text)

    def removeHostname(self):
        pass

    def scanNetwork(self):
        self.networkList.clear()
        self.networkScanWindow = NetworkScanWindow()
        self.networkScanWindow.lanScannerThread.finished.connect(self.onFinished)
        self.networkScanWindow.lanScannerThread.terminated.connect(self.onTerminated)
        self.networkScanWindow.show()
    
    def onFinished(self):
        result = self.networkScanWindow.lanScannerThread.result
        for client in result:
            self.networkList.addItem(client)

    def onTerminated(self):
        print("Terminated")
        print(self.networkScanWindow.lanScannerThread.result)