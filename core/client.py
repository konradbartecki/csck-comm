import functools
import io
import json
import logging
import pickle
import signal
import time
import xml
from datetime import datetime
from app_config import AppConfig
import socket

from csck_exceptions import CsckException
from data_service import DataService


class Client:
    def __init__(self, config:AppConfig, client_socket: socket):
        self.config = config
        self.client_socket = client_socket
        self.is_connected = False

    def start(self):
        logging.info("Connecting to: {}:{}", self.config.IPAddress, self.config.Port)
        self.client_socket.connect((self.config.IPAddress, self.config.Port))
        self.is_connected = True
        self._send_hello()
        time.sleep(1)
        self._send_dictionary()

    def send_data(self, byte_content:bytes):
        if not self.is_connected:
            raise CsckException("Socket is not connected")
        self.client_socket.sendall(byte_content)

    def close(self):
        self._graceful_shutdown_handler("closing")

    def _register_graceful_shutdown_handler(self):
        """
        Registers a handler for CTRL-C interrupt event
        """
        signal.signal(signal.SIGINT, self.__sigint_handler)

    def __sigint_handler(self, signum, frame):
        self._graceful_shutdown_handler("interrupt")

    def _graceful_shutdown_handler(self, reason: str):
        logging.warning("Shutting down client gracefully. Reason: {}", reason)
        self.is_connected = False
        self.client_socket.close()
        exit(0)

    def _send_hello(self):
        """
        Sends a handshake message
        """
        self.send_text(f"Hello from client {datetime.now()}")

    def send_text(self, text: str):
        payload_text = f"\n\n{text}"
        payload_bytes = bytes(payload_text, self.config.TextEncoding)
        self.send_data(payload_bytes)

    def _send_dictionary(self):
        generated_dictionary = DataService.get_sample_dictionary()
        logging.info("Sending dictionary: {}", repr(generated_dictionary))
        serialized = DataService.serialize(generated_dictionary, self.config.DictionarySerializationMethod)
        if type(serialized) is str:
            self.send_text(serialized)
        else:
            self.send_data(serialized)

    def _send_file(self, file_path: str):
        file_bytes = DataService.read_file_as_bytes(file_path)
        self.send_data(file_bytes)
