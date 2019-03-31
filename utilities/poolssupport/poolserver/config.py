# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 28.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Config

import os
import json

# Access to local config.json
# Maybe this can be stored later in the CGRU config.
class Config():
    ip = ""
    port = 9999
    max_clients = 32
    path = os.path.join(os.environ["CGRU_LOCATION"], "utilities", "poolssupport", "poolserver", "config.json")

    # If config does not exist, it will be created with the default settings.
    @staticmethod
    def check():
        if not os.path.isfile(Config.path):
            data = {
                "ip":"",
                "port":9999,
                "max_clients":32
            }
            Config.save(data)

    # Save config file.
    @staticmethod
    def save(data):
        with open(Config.path, "w") as outfile:
            json.dump(data, outfile, indent=4)

    # Load config file.
    @staticmethod
    def load():
        with open(Config.path) as json_file:
            data = json.load(json_file)
            Config.ip = data["ip"]
            Config.port = data["port"]
            Config.max_clients = data["max_clients"]