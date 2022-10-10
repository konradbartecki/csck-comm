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
from app_config import AppConfig, EncryptionType
import socket

from crypt_service import CryptService
from csck_exceptions import CsckException
from data_service import DataService


class Client:
    def __init__(self, config:AppConfig, client_socket: socket):
        self.config = config
        self.client_socket = client_socket
        self.is_connected = False
        self.crypt_service = CryptService()

    def start(self):
        logging.info("Connecting to: {}:{}", self.config.IPAddress, self.config.Port)
        self.client_socket.connect((self.config.IPAddress, self.config.Port))
        self.is_connected = True
        self._demo()

    def send_data(self, byte_content: bytes):
        if self.config.EncryptionType == EncryptionType.Age:
            byte_content = self.crypt_service.encrypt(byte_content)
        self._send_data_unencrypted(byte_content)

    def send_text(self, text: str):
        payload_bytes = bytes(text, self.config.TextEncoding)
        self.send_data(payload_bytes)

    def close(self):
        self._graceful_shutdown_handler("closing")

    def _demo(self):
        logging.info("Running demo scenario...")
        self._send_hello()
        time.sleep(1)
        self._send_dictionary()
        time.sleep(1)
        self._send_file()

    def _send_data_unencrypted(self, byte_content: bytes):
        if not self.is_connected:
            raise CsckException("Socket is not connected")
        self.client_socket.sendall(byte_content)

    def _send_hello(self):
        """
        Sends a handshake message that contains current local time
        """
        msg = f"Hello from client {datetime.now()}"
        logging.info("Sending hello demo message: {}", msg)
        self.send_text(msg)

    def _send_dictionary(self):
        """
        Sends a python dictionary as serialized text or binary
        """
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
        """
        Sends a magic message, that tells server
        about upcoming file's content length in bytes,
        then sends a file.

        Optionally encrypts the file if configured
        """
        if self.config.ReadFile is None:
            logging.warning("No file provided to send")
            return
        with self.config.ReadFile as f:
            file_contents = f.read()
            if self.config.EncryptionType == EncryptionType.Age:
                file_contents = self.crypt_service.encrypt(file_contents)
            magic_msg = self._get_magic_msg(file_contents)

            # Magic message should be sent in clear text
            self._send_data_unencrypted(magic_msg)
            # Contents are potentially pre-encrypted, thus can be sent in clear text
            self._send_data_unencrypted(file_contents)

    def _get_magic_msg(self, file_contents):
        """
        Generates a magic message for the server to notify it
        about the file's content length before sending a file

        Format:
        Custom-GUID-Bytes
        \n\n
        content length as unsigned big endian integer
        \n\n
        Custom-GUID-Bytes
        """
        content_length = len(file_contents)
        content_length_bit_size = content_length.bit_length()
        content_length_as_bytes = content_length.to_bytes(content_length_bit_size + 7, 'big', signed=False)
        logging.info("Sending a magic command to prepare server a file of {} bytes, ~{} kB",
                     content_length, int(content_length / 1024))
        file_cmd = bytearray(self.config.FileCommand)
        double_new_line = bytes(b'\n\n')
        magic_msg = bytearray()
        magic_msg += file_cmd
        magic_msg += double_new_line
        magic_msg += content_length_as_bytes
        magic_msg += double_new_line
        magic_msg += file_cmd
        return magic_msg

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