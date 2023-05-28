import json
from socket import socket
from common.var import MAX_PACKAGE_LENGTH, ENCODING


def get_message(sock: socket):
    data = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(data, bytes):
        json_data = data.decode(ENCODING)
        response = json.loads(json_data)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock: socket, message: dict):
    if isinstance(message, dict)
        json_message = json.dumps(message)
        encode_message = json_message.encode(ENCODING)
        sock.send(encode_message)
    else:
        raise ValueError




