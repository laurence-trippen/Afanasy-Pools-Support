# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 18.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Utils

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