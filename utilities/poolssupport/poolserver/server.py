# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Server

import socket
import sys
import threading
import json
import pymongo

def server_log(msg):
    print("[AF Pool Server]:\t" + msg)

class PoolServer():
    def bind(self, host, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_log("Binding socket to port: " + str(port))
            self.server_socket.bind((host, port))
        except socket.error as e:
            server_log("Socket error: " + str(e))
            sys.exit()

    def listen(self, max_connections):
        try:
            self.server_socket.listen(max_connections)
            while True:
                client, addr = self.server_socket.accept()
                server_log("Connection has been established [" + addr[0] + ":" + str(addr[1]) + "]")
                client.settimeout(60)
                threading.Thread(target=self.handleClient, args=(client, addr)).start()
        except socket.error as e:
            server_log("Socket error: " + str(e))
            sys.exit()
    
    def handleClient(self, client, address):
        buffer_size = 1024
        while True:
            try:
                data = client.recv(buffer_size)
                if data:
                    msg = data.decode("utf-8")
                    if msg == "get_all_pools()":
                        pass
            except:
                client.close()

if __name__ == "__main__":
    poolServer = PoolServer()
    poolServer.bind("", 9999)
    poolServer.listen(10)