# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Main

import sys
import db

from Qt import QtWidgets
from ui import MainWindow
from config import Config

def init():
    Config.check()
    Config.load()

    db.connection = db.MongoDBConnector()
    db.connection.connect("mongodb://" + Config.mongodb_host + ":" + str(Config.mongodb_port))

if __name__ == "__main__":
    init()

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())