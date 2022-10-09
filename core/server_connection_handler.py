import functools
import logging
import pprint
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
        try:
            self.receive()
            self._accept_dictionary()
            self._accept_file()
            self._chat_loop()
        except Exception as e:
            logging.warning("{} - Unhandled error {}", self.socket_id)
            print(e)
        finally:
            self._graceful_shutdown_handler("handler exiting")

    def _chat_loop(self):
        while self.is_connected:
            self.receive()

    def _accept_dictionary(self):
        received_dict = self.receive()
        deserialized_dict = DataService.deserialize(received_dict, self.config.DictionarySerializationMethod)
        logging.info("{} - Deserialized dict ({}):", self.socket_id, type(deserialized_dict))
        pprint.pprint(deserialized_dict, indent=2)
        logging.info("{} - Deserialized dict property of 'client-time': {}, type: {}",
                     self.socket_id, deserialized_dict['local_time'], type(deserialized_dict['local_time']))

    def _accept_file(self):
        if self.config.SaveFile is None:
            return

        logging.info("Waiting for a file to accept")
        received_command: bytes = self.receive(should_print=False)
        is_file_command = received_command.startswith(self.config.FileCommand)
        if not is_file_command:
            raise CsckException("Received malformed send file command")

        file_cmd = self.config.FileCommand
        double_new_line = b'\n\n'

        payload = bytearray(received_command.removeprefix(file_cmd + double_new_line))
        ending_cmd_index = payload.index(double_new_line + file_cmd, 1)
        content_length_bytes = payload[0:ending_cmd_index]
        content_length = int.from_bytes(content_length_bytes, 'big', signed=False)
        file_starts_at = ending_cmd_index + len(file_cmd) + len(double_new_line)
        remaining_file_content = payload[file_starts_at:len(payload)]
        logging.info("Will receive a file of content length {} bytes", content_length)

        file_contents = bytearray(remaining_file_content)
        while len(file_contents) < content_length:
            new_content: bytes = self.receive(should_print=False)
            file_contents += new_content
        if len(file_contents) > content_length:
            err = "Received too many bytes!"
            logging.error(err + " {} vs {}", len(file_contents), content_length)
            raise CsckException

        received_file = bytes(file_contents)
        logging.info("Accepted {} bytes, saving to {}", len(received_file), self.config.SaveFile)
        DataService.save_file(self.config.SaveFile, received_file)

    def receive(self, should_print=True):
        response = self.socket.recv(self.config.BufferSize)
        if should_print:
            logging.info("{} - Received data, {} bytes", self.socket_id, len(response))
            print(repr(response))
        if len(response) == 0:
            self._graceful_shutdown_handler("Remote connection closed")
        return response

    def send_data(self, message: bytes):
        if not self.is_connected:
            raise CsckException("Socket is not connected")
        self.socket.sendall(message)

    def _register_graceful_shutdown_handler(self):
        """
        Registers a handler for CTRL-C interrupt event
        """
        signal.signal(signal.SIGINT, self.__sigint_handler)

    def __sigint_handler(self, signum, frame):
        self._graceful_shutdown_handler("interrupt")

    def _graceful_shutdown_handler(self, reason: str):
        logging.warning("{} - Shutting down peer socket gracefully. Reason: {}", self.socket_id, reason)
        self.is_connected = False
        self.socket.close()
