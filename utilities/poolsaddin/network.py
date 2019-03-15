import socket

class LANScanner():
    mac_ports       = [22, 445, 548, 631]
    linux_ports     = [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
    windows_ports   = [135, 137, 138, 139, 445]
    # aios = [49152, 62078] # Apple iOS (ios is also the name for Cisco's OS running on their products)

    def __init__(self):
        self.hostname = socket.gethostname()
        self.networkIP = socket.gethostbyname(self.hostname)
        self.networkPrefix = self.networkIP.split(".")
        del(self.networkPrefix[-1])
        self.networkPrefix = ".".join(self.networkPrefix)

    def checkIP(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        if not s.connect_ex((ip, port)):
            s.close()
            return 1
        else:
            s.close()
    
    def startScan(self):
        print("Your IP: " + self.networkIP)
        print("Scanning LAN Network:")
        for ip in range(1, 255):
            currentIP = self.networkPrefix + '.' + str(ip)
            print(currentIP)
            for port in LANScanner.windows_ports:
                if self.checkIP(currentIP, port):
                    hostname = None
                    try:
                        hostname = socket.gethostbyaddr(currentIP)
                    except socket.herror:
                        hostname = "Hostname not found."
                    print('%s \t- %s \t- %s' % (currentIP, socket.getfqdn(currentIP), hostname))
            for port in LANScanner.linux_ports:
                if self.checkIP(currentIP, port):
                    hostname = None
                    try:
                        hostname = socket.gethostbyaddr(currentIP)
                    except socket.herror:
                        hostname = "Hostname not found."
                    print('%s \t- %s \t- %s' % (currentIP, socket.getfqdn(currentIP), hostname))
            for port in LANScanner.mac_ports:
                if self.checkIP(currentIP, port):
                    hostname = None
                    try:
                        hostname = socket.gethostbyaddr(currentIP)
                    except socket.herror:
                        hostname = "Hostname not found."
                    print('%s \t- %s \t- %s' % (currentIP, socket.getfqdn(currentIP), hostname))
        print("Scan finished!")