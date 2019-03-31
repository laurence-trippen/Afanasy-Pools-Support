# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Server

import os
import sys
import socket
import protocol
import threading
import json
import utils
import pymongo

from bson.json_util import dumps
from config import Config

# Multithreaded TCP socket server
class PoolServer():
    def __init__(self):
        self.connection_counter = 0
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
                self.connection_counter += 1
                utils.server_log("Connection has been established [" + addr[0] + ":" + str(addr[1]) + "]")
                client.settimeout(60)
                threading.Thread(target=self.handle_client, name="Connection Thread " + str(self.connection_counter),
                                 args=(client, addr)).start()
        except socket.error as e:
            utils.server_log("Socket error: " + str(e))
            sys.exit()

    # Client connection thread handler.
    # It's a simple stateless question and answer protocol like HTTP 1.1
    def handle_client(self, client, address):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    msg = json.loads(data.decode("utf-8"))
                    if msg["type"] == "request":
                        command = msg["command"]
                        if command == protocol.GET_POOLS:
                            mongo_client = pymongo.MongoClient(
                                'mongodb://' + self.mongodb_host + ":" + self.mongodb_port)
                            poolsdb = mongo_client["afpools"]
                            poolscol = poolsdb["pools"]
                            poolscol.create_index("name", unique=True)
                            pools = []
                            for pool in poolscol.find():
                                pools.append(pool)
                            pools_json = dumps(pools)
                            client.send(protocol.response(len(pools_json.encode("utf-8"))).encode("utf-8"))
                            client.send(pools_json.encode("utf-8"))
                client.close()
            except:
                client.close()


if __name__ == "__main__":
    if "CGRU_LOCATION" in os.environ:
        utils.server_log("CGRU_LOCATION=" + os.environ['CGRU_LOCATION'])
    else:
        utils.server_log("CGRU_LOCATION is not set!")
        sys.exit()

    # Loads Mongo DB config
    mongodb_config = utils.get_mongodb_config()

    # Loads pool server config
    Config.check()
    Config.load()

    # Pool server setup
    poolServer = PoolServer()
    poolServer.mongodb_host = mongodb_config["host"]
    poolServer.mongodb_port = str(mongodb_config["port"])
    poolServer.bind(Config.ip, Config.port)
    poolServer.listen(Config.max_clients)