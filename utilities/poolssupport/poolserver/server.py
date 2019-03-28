# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Server

import os
import sys
import json
import socket
import threading
import utils
import af

from bson.json_util import dumps
from config import Config

# Multithreaded TCP socket server
class PoolServer():
    def __init__(self):
        self.mongodb_host = "localhost"
        self.mongodb_port = "27017"

    # Binds the server socket to IP and Port from config.
    def bind(self, host, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            utils.server_log("Binding socket to port: " + str(port))
            self.server_socket.bind((host, port))
        except socket.error as e:
            utils.server_log("Socket error: " + str(e))
            sys.exit()

    # Listen to new incoming connections.
    # Creates a new thread per connection.
    def listen(self, max_connections):
        try:
            self.server_socket.listen(max_connections)
            while True:
                client, addr = self.server_socket.accept()
                utils.server_log("Connection has been established [" + addr[0] + ":" + str(addr[1]) + "]")
                client.settimeout(60)
                threading.Thread(target=self.handleClient, args=(client, addr)).start()
        except socket.error as e:
            utils.server_log("Socket error: " + str(e))
            sys.exit()
    
    # Client connection thread handler.
    # It's a simple stateless question and answer protocol like HTTP 1.1
    def handleClient(self, client, address):
        buffer_size = 1024
        while True:
            try:
                data = client.recv(buffer_size)
                if data:
                    msg = data.decode("utf-8")
                    if msg == "get_all_pools()":
                        af.MongoDB.connection = af.MongoDB()
                        af.MongoDB.connection.connect("mongodb://" + self.mongodb_host + ":" + self.mongodb_port)
                        pools = af.MongoDB.connection.findAllPools()
                        pools_json = dumps(pools)
                        client.send(pools_json.encode())
                        af.MongoDB.connection.close()
                client.close()
            except:
                client.close()

if __name__ == "__main__":
    # CGRU_LOCATION environment variable is needed for execution.
    if "CGRU_LOCATION" in os.environ:
        utils.server_log("CGRU_LOCATION=" + os.environ['CGRU_LOCATION'])
    else:
        utils.server_log("CGRU_LOCATION is not set!")
        sys.exit()

    # Loads MongoDB ip and port config
    mongodb_config = utils.get_mongodb_config()

    # Loads server config.
    Config.check()
    Config.load()

    # Pool Server creation.
    poolServer = PoolServer()
    poolServer.mongodb_host = mongodb_config["host"]
    poolServer.mongodb_port = mongodb_config["port"]
    poolServer.bind(Config.ip, Config.port)
    poolServer.listen(Config.max_clients)