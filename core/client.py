import functools
import io
import json
import logging
import pickle
import pprint
import signal
import time
import dict2xml
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
        self._demo()

    def _demo(self):
        logging.info("Running demo scenario...")
        self._send_hello()
        time.sleep(1)
        self._send_dictionary()
        time.sleep(1)
        self._send_file()

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
        msg = f"Hello from client {datetime.now()}"
        logging.info("Sending hello demo message: {}", msg)
        self.send_text(msg)

    def send_text(self, text: str):
        payload_bytes = bytes(text, self.config.TextEncoding)
        self.send_data(payload_bytes)

    def _send_dictionary(self):
        generated_dictionary = DataService.get_sample_dictionary()
        serialized = DataService.serialize(generated_dictionary, self.config.DictionarySerializationMethod)
        if type(serialized) is str:
            logging.info("Sending dictionary:")
            pprint.pprint(serialized, indent=2)
            self.send_text(serialized)
        else:
            logging.info("Sending binary dictionary: {}", repr(serialized))
            self.send_data(serialized)

    def _send_file(self):
        if self.config.ReadFile is None:
            logging.warning("No file provided to send")
            return
        with self.config.ReadFile as f:
            print(repr(self.config.ReadFile))
            file_contents = f.read()
            content_length = len(file_contents)
            content_length_bit_size = content_length.bit_length()
            content_length_as_bytes = content_length.to_bytes(content_length_bit_size + 7, 'big', signed=False)
            logging.info("Sending a magic command to prepare server a file of {} bytes, ~{} kB",
                         content_length, int(content_length/1024))
            file_cmd = bytearray(self.config.FileCommand)
            double_new_line = bytes(b'\n\n')
            magic_msg = bytearray()
            magic_msg += file_cmd
            magic_msg += double_new_line
            magic_msg += content_length_as_bytes
            magic_msg += double_new_line
            magic_msg += file_cmd

            self.send_data(magic_msg)
            self.send_data(file_contents)