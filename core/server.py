from datetime import datetime
import time

from app_config import AppConfig
import socket


class Server():
    def __init__(self, config:AppConfig, server_socket:socket):
        self.config = config
        self.server_socket = server_socket

    def start(self):
        print("Starting a listener at:", repr(self.config.IPAddress), repr(self.config.Port))
        self.server_socket.bind((self.config.IPAddress, self.config.Port))
        self.server_socket.listen(1)
        (conn, address) = self.server_socket.accept()
        with conn:
            self.handle_connection(conn, address)

    def handle_connection(self, conn, address):
        print('Connection from', repr(address))
        should_run = True #TODO: Support this
        while should_run:
            msg = f"Hello from server {datetime.now()}"
            payload = bytes(msg, self.config.TextEncoding)
            conn.sendall(payload)
            response = conn.recv(self.config.BufferSize)
            print("Received", repr(response))
            time.sleep(1)