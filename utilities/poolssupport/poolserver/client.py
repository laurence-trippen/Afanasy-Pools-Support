# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Client
# It's only client test code.

import socket
import protocol
import json

class PoolServerAPI():
    @staticmethod
    def get_pools():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", 9999))
            sock.sendall(protocol.request(protocol.GET_POOLS).encode("utf-8"))
            data = sock.recv(1024)
            if data:
                msg = json.loads(data.decode("utf-8"))
                if msg["type"] == "response":
                    size = msg["size"]
                    data = sock.recv(size)
                    if data:
                        print(data.decode("utf-8"))
                        return data.decode("utf-8")

if __name__ == "__main__":
    pools = PoolServerAPI.get_pools()
    print(pools)
