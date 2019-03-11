# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Main

import sys
import db

from Qt import QtWidgets
from ui import MainWindow
from model import AF_API
from config import Config

dbConnection = None

def init():
    dbConnection = db.MongoDBConnector()
    dbConnection.connect("mongodb://192.168.1.107:27017")

    Config.check()
    Config.load()

    print(Config.mongodb_host)
    print(Config.mongodb_port)

if __name__ == "__main__":
    init()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())