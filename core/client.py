from datetime import datetime
import time

from app_config import AppConfig
import socket


class Client():
    def __init__(self, config:AppConfig, client_socket:socket):
        self.config = config
        self.client_socket = client_socket


    def start(self):
        print("Connecting to:", repr(self.config.IPAddress), repr(self.config.Port))
        should_run = True #TODO: Support this
        self.client_socket.connect((self.config.IPAddress, self.config.Port))
        while should_run:
            msg = f"Hello from client {datetime.now()}"
            payload = bytes(msg, self.config.TextEncoding)
            self.client_socket.sendall(payload)
            response = self.client_socket.recv(self.config.BufferSize)
            print("Received", repr(response))
            time.sleep(1)
