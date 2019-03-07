import pymongo
from model import AF_RenderPool, AF_RenderClient

class MongoDBConnector():
    db_name = "afpools"
    col_name = "pools"

    def __init__(self):
        pass

    def connect(self, connection):
        pool1 = AF_RenderPool("Standard Pool")
        pool1.clients.append(AF_RenderClient("lt-pc-01", "CGRU 2.2.3", "127.0.0.1", "27017"))
        pool1.clients.append(AF_RenderClient("lt-pc-02", "CGRU 2.2.3", "192.168.0.101", "27017"))

        self.client = pymongo.MongoClient(connection)
        self.afpools_db = self.client[MongoDBConnector.db_name]
        self.pools_col = self.afpools_db[MongoDBConnector.col_name]
        
        x = self.pools_col.insert_one(self.poolToJSON(pool1))
        print(x.inserted_id)

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
