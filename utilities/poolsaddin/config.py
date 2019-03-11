# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 11.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Manager - Config

import os
import json

class Config():
    mongodb_host = 'localhost'
    mongodb_port = 27017

    @staticmethod
    def check():
        if not os.path.isfile("config.json"):
            data = {
                "mongodb_host":"localhost",
                "mongodb_port":27017
            }
            Config.save(data)

    @staticmethod
    def save(data):
        with open("config.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

    @staticmethod
    def load():
        with open('config.json') as json_file:
            data = json.load(json_file)
            Config.mongodb_host = data["mongodb_host"]
            Config.mongodb_port = data["mongodb_port"]