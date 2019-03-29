import json

GET_POOLS = "GET POOLS"


def request(command):
    req = {
        "type": "request",
        "command": command
    }
    return json.dumps(req)


def response(size):
    res = {
        "type": "response",
        "size": size
    }
    return json.dumps(res)