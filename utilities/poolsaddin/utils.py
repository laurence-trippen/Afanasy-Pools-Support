# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 18.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Utils

from Qt import QtCore

# Checks if item string is in QListWidget
def hasQListWidgetText(qList, text):
    if qList.count() > 0:
        i = 0
        while i < qList.count():
            item = qList.item(i)
            if item.text() == text:
                return True
            i += 1
    return False

# Makes this "$hostname ($ip)" to this "$hostname".
# Example: "PC-01 (127.0.0.1)" -> "PC-01" 
def parseHostnameFromFormat(hostnameAndIP):
    hostname = hostnameAndIP[0:hostnameAndIP.find("(")]
    return hostname.replace(" ", "")

# Returns all items of QListWidget
def getQListWidgetItems(qList):
    items = []
    if qList.count() > 0:
        i = 0
        while i < qList.count():
            item = qList.item(i)
            items.append(item)
            i += 1
    return items

# Filters for enabled and checked client items.
def filterForCheckedAndEnabledItems(clientsItems):
    items = []
    for clientItem in clientsItems:
        flags = clientItem.flags()
        checkState = clientItem.checkState()
        if flags & QtCore.Qt.ItemIsEnabled and checkState == QtCore.Qt.Checked:
            items.append(clientItem)
    return items