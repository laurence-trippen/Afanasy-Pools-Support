# UTF-8

import os
import sys

from Qt import QtCore, QtGui, QtWidgets

import cgruutils

# Create Pool Window / Modal Form
class CreatePoolDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CreatePoolDialog, self).__init__(parent)

        self.setWindowTitle("Create Pool")

        # Window icon
        iconpath = cgruutils.getIconFileName('afanasy')
        if iconpath is not None:
            self.setWindowIcon(QtGui.QIcon(iconpath))

        self.setFixedSize(400, 60)
        self.setModal(True)

        poolNameLineEdit = QtWidgets.QLineEdit()
        poolNameLineEdit.setPlaceholderText("Pool name")

        createPoolButton = QtWidgets.QPushButton("Create Pool")

        topLayout = QtWidgets.QHBoxLayout(self)
        topLayout.addWidget(poolNameLineEdit)
        topLayout.addWidget(createPoolButton)
    
    def createPool(self):
        pass

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
            self.setWindowIcon(QtGui.QIcon(iconpath))

        poolsLabel = QtWidgets.QLabel("Pools")

        poolsList = QtWidgets.QListWidget()
        poolsList.addItem("Pool 1")

        createPoolButton = QtWidgets.QPushButton("Create")
        createPoolButton.clicked.connect(self.showCreatePoolDialog)

        deletePoolButton = QtWidgets.QPushButton("Delete")
        editPoolButton = QtWidgets.QPushButton("Edit")

        poolsButtonLayout = QtWidgets.QHBoxLayout()
        poolsButtonLayout.addWidget(createPoolButton)
        poolsButtonLayout.addWidget(editPoolButton)
        poolsButtonLayout.addWidget(deletePoolButton)

        poolsLayout = QtWidgets.QVBoxLayout()
        poolsLayout.addWidget(poolsLabel)
        poolsLayout.addWidget(poolsList)
        poolsLayout.addLayout(poolsButtonLayout)

        clientsLabel = QtWidgets.QLabel("Clients")
        
        clientsList = QtWidgets.QListWidget()
        clientsList.addItem("Client 01")

        addClientButton = QtWidgets.QPushButton("Add Client")
        removeClientButton = QtWidgets.QPushButton("Remove Client")

        clientsButtonLayout = QtWidgets.QHBoxLayout()
        clientsButtonLayout.addWidget(addClientButton)
        clientsButtonLayout.addWidget(removeClientButton)

        clientsLayout = QtWidgets.QVBoxLayout()
        clientsLayout.addWidget(clientsLabel)
        clientsLayout.addWidget(clientsList)
        clientsLayout.addLayout(clientsButtonLayout)

        listsLayout = QtWidgets.QHBoxLayout()
        listsLayout.addLayout(poolsLayout)
        listsLayout.addLayout(clientsLayout)

        # Top Root Layout
        topLayout = QtWidgets.QVBoxLayout(self)
        topLayout.addLayout(listsLayout)
    
    def showCreatePoolDialog(self):
        self.createPoolDialog = CreatePoolDialog()
        self.createPoolDialog.exec_()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())