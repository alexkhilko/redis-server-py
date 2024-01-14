#!/usr/bin/env python3

import socket
from resp.parsers import serialize
from commands import handle_request
import time

HOST = "127.0.0.1"
PORT = 6379


def _encode_response(response: list) -> bytes:
    return serialize(response).encode("utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("after bind")
    s.listen()
    print("after listen")
    while True:
        conn, addr = s.accept()
        print("after accept")
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            print(f"received data {data}")
            if not data:
                time.sleep(2)
                continue
            response = handle_request(data)
            conn.sendall(_encode_response(response))
