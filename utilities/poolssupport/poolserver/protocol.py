# Encoding: UTF-8
# Author: Laurence Trippen
# Date: 25.03.2019
# E-Mail: laurence.trippen@gmail.com
# Program: Afanasy Pool Server - Network protocol
# Defines the rules of a simple stateless request/response network
# protocol based on TCP.

import json

# Get pools command
GET_POOLS = "GET POOLS"

# Generates a json request
def request(command):
    req = {
        "type": "request",
        "command": command
    }
    return json.dumps(req)

# Generates a json response
def response(size):
    res = {
        "type": "response",
        "size": size
    }
    return json.dumps(res)