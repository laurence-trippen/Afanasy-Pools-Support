# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - MongoDB Access

import pymongo
from model import AF_RenderPool, AF_RenderClient

connection = None

class MongoDBConnector():
    db_name = "afpools"
    col_name = "pools"

    def __init__(self):
        pass

    def connect(self, connection):
        try:
            self.client = pymongo.MongoClient(connection)
            print("DB connection established!")
        except:
            print("DB connection failed!")

        self.afpools_db = self.client[MongoDBConnector.db_name]
        self.pools_col = self.afpools_db[MongoDBConnector.col_name]
        self.pools_col.create_index("name", unique=True)

    def insertPool(self, pool):
        try:
            result = self.pools_col.insert_one(self.poolToJSON(pool))
            return result.matched_count > 0
        except pymongo.errors.PyMongoError as e:
            return False, e

    def poolToJSON(self, pool):
        poolDict = {
            "name" : pool.name
        }
        clients = []
        for client in pool.clients:
            clients.append(self.clientToJSON(client))
        poolDict["clients"] = clients
        return poolDict

    def clientToJSON(self, client):
        clientDict = {
            "hostname": client.hostname,
            "engine": client.engine,
            "ip": client.ip,
            "port": client.port
        }
        return clientDict
