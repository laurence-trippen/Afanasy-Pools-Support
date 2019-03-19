# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - User Interface

import os
import db
import utils
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

        # Pools List
        self.poolsLabel = QtWidgets.QLabel("Pools")
        self.poolsList = QtWidgets.QListWidget()
        self.poolsList.itemClicked.connect(self.onPoolClicked)

        # Create Pool Button
        self.createPoolButton = QtWidgets.QPushButton("Create")
        self.createPoolButton.clicked.connect(self.createPool)

        # Edit Pool Button
        self.editPoolButton = QtWidgets.QPushButton("Edit")
        self.editPoolButton.clicked.connect(self.editPool)
        
        # Delete Pool Button
        self.deletePoolButton = QtWidgets.QPushButton("Delete")
        self.deletePoolButton.clicked.connect(self.deletePool)

        self.poolsButtonLayout = QtWidgets.QHBoxLayout()
        self.poolsButtonLayout.addWidget(self.createPoolButton)
        self.poolsButtonLayout.addWidget(self.editPoolButton)
        self.poolsButtonLayout.addWidget(self.deletePoolButton)

        self.poolsLayout = QtWidgets.QVBoxLayout()
        self.poolsLayout.addWidget(self.poolsLabel)
        self.poolsLayout.addWidget(self.poolsList)
        self.poolsLayout.addLayout(self.poolsButtonLayout)

        # Clients List
        self.clientsLabel = QtWidgets.QLabel("Clients")
        self.clientsList = QtWidgets.QListWidget()

        # Add Client Button
        self.addClientButton = QtWidgets.QPushButton("Add Client(s)")
        self.addClientButton.clicked.connect(self.addClient)

        # Remove Client Button
        self.removeClientButton = QtWidgets.QPushButton("Remove Client")
        self.removeClientButton.clicked.connect(self.removeClient)

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
        self.loadPools()

    # UI Menubar setup
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
    
    # UI Statusbar setup
    def initStatusBar(self):
        self.statusbar = QtGui.QStatusBar()
        self.statusbar.showMessage(db.MongoDBConnector.status)
        self.topLayout.addWidget(self.statusbar)

    # Loads pools from database.
    def loadPools(self):
        self.pools = db.connection.findAllPools()
        for pool in self.pools:
            self.poolsList.addItem(pool.name)
    
    # Refreshs the pools list.
    def update(self):
        print("Update")
        self.poolsList.clear()
        self.loadPools()

    # Create Pool
    def createPool(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Create Pool', 'Pool Name')
        if ok and str(text) != "":
            pool = AF_RenderPool(text)
            result = db.connection.insertPool(pool)
            if result["acknowledged"]:
                self.update()
            else:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setWindowTitle("Error")
                msgBox.setText(str(result["e"]))
                msgBox.exec_()

    # Edit Pool
    def editPool(self):
        currentItem = self.poolsList.currentItem()
        text, ok = QtGui.QInputDialog.getText(self, "New Pool Name", "New Pool Name", text=currentItem.text())
        if ok and str(text) != "":
            result = db.connection.updatePoolName(currentItem.text(), text)
            if result["acknowledged"]:
                self.update()
            else:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setWindowTitle("Error")
                msgBox.setText(str(result["e"]))
                msgBox.exec_()

    # Delete Pool
    def deletePool(self):
        currentItem = self.poolsList.currentItem()
        flags = QtGui.QMessageBox.StandardButton.Yes
        flags |= QtGui.QMessageBox.StandardButton.No
        question = "Do you realy want to delete the pool '" + currentItem.text() + "'?"
        response = QtGui.QMessageBox.question(self, "Question", question, flags)
        if response == QtGui.QMessageBox.Yes:
            result = db.connection.deletePool(currentItem.text())
            if result["acknowledged"]:
                self.update()

    # Add Client
    def addClient(self):
        if self.selected_pool != None:
            self.addClientWindow = AddClientWindow(self.selected_pool)
            self.addClientWindow.closed.connect(self.update)
            self.addClientWindow.show()
        else:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setWindowTitle("Information")
            msgBox.setText("No pool selected!")
            msgBox.exec_()
    
    # Remove Client
    def removeClient(self):
        pass

    # Updates the clients list with selected pool clients.
    # self.selected_pool is set by clicking on item.
    def onPoolClicked(self, item):
        for pool in self.pools:
            if pool.name == item.text():
                self.selected_pool = pool
                self.clientsList.clear()
                for client in pool.clients:
                    self.clientsList.addItem(client.hostname)

# Network scan progress window.
class NetworkScanWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setFixedSize(340, 60)
        self.initUI()

        # LAN Scanner thread setup & binding to UI.
        self.lanScannerThread = LANScanner()
        self.lanScannerThread.updateProgress.connect(self.setProgress)
        self.lanScannerThread.finished.connect(self.onFinished)
        self.lanScannerThread.terminated.connect(self.onTerminated)
        self.lanScannerThread.start()
    
    # UI setup
    def initUI(self):
        # Modality
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Window Title
        self.setWindowTitle("Scanning network for hosts ...")
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))
        
        # ProgessBar
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.minimum = 1
        self.progressBar.maximum = 100

        # Root node.
        self.topLayout = QtWidgets.QHBoxLayout(self)
        self.topLayout.addWidget(self.progressBar)
    
    # Updates the progressbar
    def setProgress(self, progress):
        self.progressBar.setValue(progress)

    # If thread finished the window close automatically
    def onFinished(self):
        self.close()
    
    # If thread terminated (canceled) the window close automatically.
    def onTerminated(self):
        self.close()

# Add Client Dialog/Window
class AddClientWindow(QtWidgets.QWidget):
    closed = QtCore.Signal()
    def __init__(self, selected_pool):
        QtWidgets.QWidget.__init__(self)
        self.initSelectedPool(selected_pool)
        self.initUI()
        self.loadAFClients()
        self.loadLastScan()

    # On widget close() emits the closed signal.
    def closeEvent(self, event):
        self.closed.emit()

    def initSelectedPool(self, selected_pool):
        self.selected_pool = selected_pool
        self.pool_hostnames = []
        for client in selected_pool.clients:
            self.pool_hostnames.append(client.hostname)

    # UI Initialization
    def initUI(self):
        self.setFixedSize(780, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        # Window Title
        self.setWindowTitle("Add Client(s)")
        
        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))

        # Network Scan List
        self.networkList = QtWidgets.QListWidget()
        self.scanNetworkButton = QtWidgets.QPushButton("Scan Network")
        self.scanNetworkButton.clicked.connect(self.scanNetwork)
        
        self.networkLayout = QtWidgets.QVBoxLayout()
        self.networkLayout.addWidget(self.networkList)
        self.networkLayout.addWidget(self.scanNetworkButton)

        self.networkGroupBox = QtWidgets.QGroupBox("Local Network")
        self.networkGroupBox.setLayout(self.networkLayout)

        # Add Hostname Button
        self.addHostnameButton = QtWidgets.QPushButton("(+) Hostname")
        self.addHostnameButton.clicked.connect(self.addHostname)

        # Remove Hostname Button
        self.remHostnameButton = QtWidgets.QPushButton("(-) Hostname")
        self.remHostnameButton.clicked.connect(self.removeHostname)

        self.hostnamesButtonsLayout = QtWidgets.QHBoxLayout()
        self.hostnamesButtonsLayout.addWidget(self.addHostnameButton)
        self.hostnamesButtonsLayout.addWidget(self.remHostnameButton)

        # Hostname List
        self.hostnamesList = QtWidgets.QListWidget()
        self.hostnamesLayout = QtWidgets.QVBoxLayout()
        self.hostnamesLayout.addWidget(self.hostnamesList)
        self.hostnamesLayout.addLayout(self.hostnamesButtonsLayout)

        self.hostnamesGroupBox = QtWidgets.QGroupBox("Hostnames")
        self.hostnamesGroupBox.setLayout(self.hostnamesLayout)

        # Afanasy Clients List
        self.clientsList = QtWidgets.QListWidget()

        self.clientsLayout = QtWidgets.QVBoxLayout()
        self.clientsLayout.addWidget(self.clientsList)

        self.clientsGroupBox = QtWidgets.QGroupBox("Afanasy Clients")
        self.clientsGroupBox.setLayout(self.clientsLayout)
       
        self.groupBoxesLayout = QtWidgets.QHBoxLayout()
        self.groupBoxesLayout.addWidget(self.clientsGroupBox)
        self.groupBoxesLayout.addWidget(self.hostnamesGroupBox)
        self.groupBoxesLayout.addWidget(self.networkGroupBox)

        # Save Button
        self.saveButton = QtWidgets.QPushButton("Save")
        self.saveButton.clicked.connect(self.save)

        # Root node
        self.topLayout = QtWidgets.QVBoxLayout(self)
        self.topLayout.addLayout(self.groupBoxesLayout)
        self.topLayout.addWidget(self.saveButton)

    # Checks if client is already in pool.
    # If true then make the client not addable.
    def isClientInSelectedPool(self, af_client):
        for client in self.selected_pool.clients:
            if af_client.hostname == client.hostname:
                return True
        return False
    
    # Checks if hostname is already in pool.
    def isHostnameInSelectedPool(self, hostname):
        for client in self.selected_pool.clients:
            if hostname == client.hostname:
                return True
        return False

    # Loads the Afanasy clients.
    def loadAFClients(self):
        self.af_clients = AF_API.request_renderclients()
        for af_client in self.af_clients:
            if self.isClientInSelectedPool(af_client):
                item = QtGui.QListWidgetItem(af_client.hostname + " (" + af_client.ip + ")")
                item.setCheckState(QtCore.Qt.Checked)
                item.setFlags(QtCore.Qt.NoItemFlags)
                self.clientsList.addItem(item)
            else:
                item = QtGui.QListWidgetItem(af_client.hostname + " (" + af_client.ip + ")")
                item.setCheckState(QtCore.Qt.Unchecked)
                self.clientsList.addItem(item)

    # Add hostname
    def addHostname(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Add Hostname', 'Hostname')
        if ok and str(text) != "":
            if text in self.pool_hostnames or utils.hasQListWidgetText(self.hostnamesList, text):
                msgBox = QtGui.QMessageBox(self)
                msgBox.setWindowTitle("Warning!")
                msgBox.setText("Hostname already exists!")
                msgBox.exec_()
            else:
                self.hostnamesList.addItem(text)

    # Remove hostname
    def removeHostname(self):
        self.hostnamesList.takeItem(self.hostnamesList.currentRow())

    # Shows the network scan window and starts thread worker.
    def scanNetwork(self):
        self.networkList.clear()
        self.networkScanWindow = NetworkScanWindow()
        self.networkScanWindow.lanScannerThread.finished.connect(self.onFinished)
        self.networkScanWindow.lanScannerThread.terminated.connect(self.onTerminated)
        self.networkScanWindow.show()

    # Network segment scan on finished callback.
    def onFinished(self):
        result = self.networkScanWindow.lanScannerThread.result
        for client in result:
            item = QtGui.QListWidgetItem(client)
            hostname = utils.parseHostnameFromFormat(client)
            if "Hostname not found." in client:
                item.setFlags(QtCore.Qt.NoItemFlags)
            item.setCheckState(QtCore.Qt.Unchecked)
            if self.isHostnameInSelectedPool(hostname):
                item.setFlags(QtCore.Qt.NoItemFlags)
                item.setCheckState(QtCore.Qt.Checked)
            self.networkList.addItem(item)

    # Network segment scan on terminated callback.
    def onTerminated(self):
        print("Terminated")
        print(self.networkScanWindow.lanScannerThread.result)
    
    # Checks if the network has already been scanned.
    # If so then load the last scan.
    # This is very resource-saving and time efficient.
    def loadLastScan(self):
        last_result = LANScanner.last_scan_result
        for client in last_result:
            item = QtGui.QListWidgetItem(client)
            if "Hostname not found." in client:
                item.setFlags(QtCore.Qt.NoItemFlags)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.networkList.addItem(item)
    
    # Returns all hostnames from hostnames QListWidget
    def getHostnames(self):
        hostnames = []
        if self.hostnamesList.count() > 0:
            i = 0
            while i < self.hostnamesList.count():
                item = self.hostnamesList.item(i)
                hostnames.append(item.text())
                i += 1
        return hostnames

    # Adds the selected Afanasy clients & hostnames.
    def save(self):
        # All selected clients for database insert.
        consolidatedClients = []

        # Add all hostname strings to consolidatedClients[]
        hostnames = self.getHostnames()
        for hostname in hostnames:
            if not hostname in consolidatedClients:
                consolidatedClients.append(hostname)
        
        # Add all selected afanasy clients to consolidatedClients[]
        filterAfClients = utils.filterForCheckedAndEnabledItems(utils.getQListWidgetItems(self.clientsList))
        for client in filterAfClients:
            hostname = utils.parseHostnameFromFormat(client.text())
            if not hostname in consolidatedClients:
                consolidatedClients.append(hostname)
        
        # Add all selected network clients to consolidatedClients[]
        filteredNetClients = utils.filterForCheckedAndEnabledItems(utils.getQListWidgetItems(self.networkList))
        for client in filteredNetClients:
            hostname = utils.parseHostnameFromFormat(client.text())
            if not hostname in consolidatedClients:
                consolidatedClients.append(hostname)
        
        # Pushs clients to selected pool in database.
        for hostname in consolidatedClients:
            result = db.connection.pushClientToPool(self.selected_pool.name, AF_RenderClient(hostname, "", "", ""))
            if not result["acknowledged"]:
                msgBox = QtGui.QMessageBox(self)
                msgBox.setWindowTitle("Error")
                msgBox.setText(str(result["e"]))
                msgBox.exec_()
        
        self.close()