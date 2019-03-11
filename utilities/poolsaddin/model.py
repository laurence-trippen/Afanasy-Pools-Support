# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 06.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Model Classes

import af

class AF_RenderClient():
    def __init__(self, hostname, engine, ip, port):
        self.hostname = hostname
        self.engine = engine
        self.ip = ip
        self.port = port

class AF_RenderPool():
    def __init__(self, name):
        self.name = name
        self.clients = []

class AF_API():
    @staticmethod
    def request_renderclients():
        client_list = []
        cmd = af.Cmd()
        clients = cmd.renderGetList()
        for client in clients:
            name = client['name']
            version = client['engine']
            address = client['address']
            ip = address['ip']
            port = address['port']
            client_list.append(AF_RenderClient(name, version, ip, port))
        return client_list