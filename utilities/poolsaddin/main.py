# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Main

import os
import sys
import db
import network

from Qt import QtWidgets
from ui import MainWindow
from config import Config

if __name__ == "__main__":
    if "CGRU_LOCATION" in os.environ:
        print("CGRU_LOCATION=" + os.environ['CGRU_LOCATION'])
    else:
        print("CGRU_LOCATION is not set!")
        sys.exit()

    # network.LANScanner().startScan()

    Config.check()
    Config.load()

    db.connection = db.MongoDBConnector()
    db.connection.connect("mongodb://" + Config.mongodb_host + ":" + str(Config.mongodb_port))
    
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())