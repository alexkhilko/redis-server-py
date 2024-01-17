#!/usr/bin/env python3

import socket
from request_handler import process_request
import logging
import threading

logger = logging.getLogger(__name__)


HOST = "127.0.0.1"
PORT = 6379


def handle_client(connection):
    with connection:
        while True:
            # print(f"Connected by {address}")
            data = connection.recv(1024)
            # print(f"received data {data}")
            if not data:
                break
            response = process_request(data)
            connection.sendall(response)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((HOST, PORT))
    lsock.listen()
    while True:
        client_socket, address = lsock.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
