import functools
import logging
import signal
import socket
from datetime import datetime
from app_config import AppConfig
from csck_exceptions import CsckException
from data_service import DataService


class ServerConnectionHandler:
    def __init__(self, new_connection_socket: socket, config: AppConfig):
        self.socket = new_connection_socket
        self.config = config
        self.is_connected = self.socket
        self.socket_id = new_connection_socket.getpeername()

    def handle(self):
        # Expect hello message
        self.receive()
        # Expect dictionary
        received_dict = self.receive()
        deserialized_dict = DataService.deserialize(received_dict, self.config.DictionarySerializationMethod)
        proper_dict = dict(deserialized_dict)
        logging.info("{} - Deserialized dict: {}", self.socket_id, repr(proper_dict))
        logging.info("{} - Deserialized dict property of 'client-time': {}", self.socket_id, proper_dict['local_time'])
        logging.info("{} - Type of deserialized dict is {}", self.socket_id, type(deserialized_dict))

        while self.is_connected:
            self.receive()

    def receive(self):
        response = self.socket.recv(self.config.BufferSize)
        logging.info("{} - Received data, {} bytes", self.socket_id, len(response))
        print(repr(response))
        if len(response) == 0:
            self._graceful_shutdown_handler("Remote connection closed")
        return response

    def send_data(self, message: bytes):
        if not self.is_connected:
            raise CsckException("Socket is not connected")
        self.socket.sendall(message)

    def _graceful_shutdown_handler(self, reason: str):
        logging.warning("{} - Shutting down peer socket gracefully. Reason: {}", self.socket_id, reason)
        self.is_connected = False
        self.socket.close()
