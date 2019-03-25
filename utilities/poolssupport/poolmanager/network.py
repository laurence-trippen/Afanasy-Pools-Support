# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 15.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Network

import socket

from Qt import QtCore

# Scans the local network segment (TCP 3-Way-Handshake)
class LANScanner(QtCore.QThread):
    # Destination ports.
    # Probably too many ports, which slows down the scan. :-(
    MAC_PORTS       = [22, 445, 548, 631]
    LINUX_PORTS     = [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
    WINDOWS_PORTS   = [135, 137, 138, 139, 445]

    updateProgress = QtCore.Signal(int)     # Update singal
    last_scan_result = []                   # Result cache

    # Constructor
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.result = []
        self.hostname = socket.gethostname()
        self.networkIP = socket.gethostbyname(self.hostname)
        self.networkPrefix = self.networkIP.split(".")
        del(self.networkPrefix[-1])
        self.networkPrefix = ".".join(self.networkPrefix)

    # Socket connection check. Hello?
    def checkIP(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        if not s.connect_ex((ip, port)):
            s.close()
            return 1
        else:
            s.close()
    
    # Parse and hostname formatting.
    def parseAndFormatHostname(self, hostname):
        return hostname[hostname.find("'")+1:hostname.find("',")]

    # Get Hostname by IP address.
    def getHostname(self, ip):
        hostname = None
        try:
            hostname = self.parseAndFormatHostname(str(socket.gethostbyaddr(ip)))
            if ".localdomain" in hostname:
                hostname = hostname.replace(".localdomain", "")
        except socket.herror:
            hostname = "Hostname not found."
        return hostname

    '''
    Progress percentage calculation:

    total = 276
    step = 100 / total
    progress = 0

    for i in range(1, total):
        progress += step
        print(str(int(round(progress))) + "%")
    '''

    # Thread code.
    def run(self):
        win_ports_len = len(LANScanner.WINDOWS_PORTS)
        mac_ports_len = len(LANScanner.MAC_PORTS)
        lin_ports_len = len(LANScanner.LINUX_PORTS)
        total = win_ports_len + mac_ports_len + lin_ports_len + 255
        step = 100 / total
        progress = 0

        for ip in range(1, 255):
            currentIP = self.networkPrefix + '.' + str(ip)
            progress += step
            self.updateProgress.emit(progress)
            for port in LANScanner.WINDOWS_PORTS:
                if self.checkIP(currentIP, port):
                    host_entry = self.getHostname(currentIP) + " (" + currentIP + ")"
                    if not host_entry in self.result:
                        self.result.append(host_entry)
                    progress += step
                    self.updateProgress.emit(progress)
            for port in LANScanner.LINUX_PORTS:
                if self.checkIP(currentIP, port):
                    host_entry = self.getHostname(currentIP) + " (" + currentIP + ")"
                    if not host_entry in self.result:
                        self.result.append(host_entry)
                    progress += step
                    self.updateProgress.emit(progress)
            for port in LANScanner.MAC_PORTS:
                if self.checkIP(currentIP, port):
                    host_entry = self.getHostname(currentIP) + " (" + currentIP + ")"
                    if not host_entry in self.result:
                        self.result.append(host_entry)
                    progress += step
                    self.updateProgress.emit(progress)
        self.updateProgress.emit(100)
        LANScanner.last_scan_result = self.result