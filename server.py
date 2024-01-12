#!/usr/bin/env python3

import socket
from resp.parsers import deserialize, serialize

HOST = "127.0.0.1"
PORT = 6379


def parse_request(request: bytes) -> str:
    return deserialize(request.decode("utf-8"))


def handle_request(command: str, *arguments) -> list:
    if command == "PING":
        return ["PONG"]
    if command == "ECHO":
        return arguments
    raise ValueError(f"Unknown command {command}")


def _encode_response(response: list) -> bytes:
    return serialize(response).encode("utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("after bind")
    s.listen()
    print("after listen")
    conn, addr = s.accept()
    print("after accept")
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print(f"received data {data}")
            if not data:
                break
            request = parse_request(data)
            response = handle_request(*request)
            conn.sendall(_encode_response(response))
