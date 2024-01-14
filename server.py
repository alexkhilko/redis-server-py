#!/usr/bin/env python3

import socket
from resp.parsers import serialize
from commands import handle_request
import time
from exceptions import RedisServerException
import logging

logger = logging.getLogger(__name__)


HOST = "127.0.0.1"
PORT = 6379


def _encode_response(response: list) -> bytes:
    return serialize(response).encode("utf-8")

def _encode_error_response(error) -> bytes:
    return serialize([error], is_error=True).encode("utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    conn, addr = lsock.accept()
    with conn:
        while True:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            print(f"received data {data}")
            if not data:
                time.sleep(2)
                continue
            try:
                response = handle_request(data)
            except RedisServerException as exc:
                logger.exception("Redis exception - %s", exc)
                response = _encode_error_response(str(exc))
            else:
                response = _encode_response(response)
            conn.sendall(response)
