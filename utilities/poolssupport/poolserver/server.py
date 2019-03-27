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
import af

from bson.json_util import dumps

def get_mongodb_config():
    path = os.path.join(os.environ["CGRU_LOCATION"], "utilities", "poolssupport", "poolmanager", "config.json")
    config = {
        "host":"localhost",
        "port":"27017"
    }
    with open(path) as json_file:
        data = json.load(json_file)
        config["host"] = data["mongodb_host"]
        config["port"] = data["mongodb_port"]
    return config

def server_log(msg):
    print("[AF Pool Server]:\t" + msg)

class PoolServer():
    def __init__(self):
        self.mongodb_host = "localhost"
        self.mongodb_port = "27017"

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
                        af.MongoDB.connection = af.MongoDB()
                        af.MongoDB.connection.connect("mongodb://" + self.mongodb_host + ":" + self.mongodb_port)
                        pools = af.MongoDB.connection.findAllPools()
                        pools_json = dumps(pools)
                        client.send(pools_json.encode())
                client.close()
            except:
                client.close()

if __name__ == "__main__":
    if "CGRU_LOCATION" in os.environ:
        server_log("CGRU_LOCATION=" + os.environ['CGRU_LOCATION'])
    else:
        server_log("CGRU_LOCATION is not set!")
        sys.exit()

    mongodb_config = get_mongodb_config()

    poolServer = PoolServer()
    poolServer.mongodb_host = mongodb_config["host"]
    poolServer.mongodb_port = mongodb_config["port"]
    poolServer.bind("", 9999)
    poolServer.listen(10)