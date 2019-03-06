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
            self.setWindowIcon(QtGui.QIcon(iconpath))

        poolsLabel = QtWidgets.QLabel("Pools")

        poolsList = QtWidgets.QListWidget()
        poolsList.addItem("Pool 1")

        createPoolButton = QtWidgets.QPushButton("Create")
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

        addClientButton = QtWidgets.QPushButton("Add")
        removeClientButton = QtWidgets.QPushButton("Remove")

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

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec_())