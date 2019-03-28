# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 28.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Utils

import os
import json

# Reads poolmanager's config to access MongoDB address.
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

# Simple global print format function
def server_log(msg):
    print("[AF Pool Server]:\t" + msg)