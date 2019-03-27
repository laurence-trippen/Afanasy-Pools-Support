# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Client

import socket
import sys

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Failed to connect!")
    sys.exit()

print("Socket created!")

host = "www.google.com"
port = 80

try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Hostname could not be resolved!")
    sys.exit()

print("IP Address: " + remote_ip)

sock.connect((remote_ip, port))