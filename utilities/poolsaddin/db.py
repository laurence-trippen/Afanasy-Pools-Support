# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 11.03.2019
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
            result = self.pools_col.insert_one(self.convertPool(pool))
            return { "acknowledged" : result.acknowledged, "e" : None }
        except pymongo.errors.PyMongoError as e:
            return { "acknowledged" : False, "e" : e }
    
    def deletePool(self, poolName):
        try:
            result = self.pools_col.delete_one({ "name" : poolName })
            return { "acknowledged" : result.acknowledged, "e" : None }
        except pymongo.errors.PyMongoError as e:
            return { "acknowledged" : result.acknowledged, "e" : e }

    def findAllPools(self):
        pools = []
        for pool in self.pools_col.find():
            pools.append(self.convertPool(pool))
        return pools

    def convertPool(self, pool):
        if isinstance(pool, AF_RenderPool):
            poolDict = {
                "name" : pool.name
            }
            clients = []
            for client in pool.clients:
                clients.append(self.convertClient(client))
            poolDict["clients"] = clients
            return poolDict
        elif isinstance(pool, dict):
            renderpool = AF_RenderPool(pool["name"])
            dictClients = pool["clients"]
            for client in dictClients:
                renderpool.clients.append(self.convertClient(client))
            return renderpool
            
    def convertClient(self, client):
        if isinstance(client, AF_RenderClient):
            clientDict = {
                "hostname": client.hostname,
                "engine": client.engine,
                "ip": client.ip,
                "port": client.port
            }
            return clientDict
        elif isinstance(client, dict):
            return AF_RenderClient(
                client["hostname"],
                client["engine"],
                client["ip"],
                client["port"]
            )