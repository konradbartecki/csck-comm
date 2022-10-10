import functools
import logging
import pprint
import signal
import socket
import traceback
from app_config import AppConfig, EncryptionType
from crypt_service import CryptService
from csck_exceptions import CsckException
from data_service import DataService


class ServerConnectionHandler:
    def __init__(self, new_connection_socket: socket, config: AppConfig):
        self.socket = new_connection_socket
        self.config = config
        self.is_connected = self.socket
        self.socket_id = new_connection_socket.getpeername()
        self.crypt_service = CryptService()

    def handle(self):
        try:
            self._handle_demo()
            self._chat_loop()
        except Exception as e:
            logging.warning("{} - Unhandled error", self.socket_id)
            print(str(e))
            traceback.print_exc()
        finally:
            self._graceful_shutdown_handler("handler exiting")

    def receive_data(self, should_print=True):
        response = self._receive_data_unencrypted(should_print)
        if self.config.EncryptionType == EncryptionType.Age:
            response = self.crypt_service.decrypt(response)
            if should_print:
                logging.info("Decrypted content: {}", repr(response))
        return response

    def _receive_data_unencrypted(self, should_print=True):
        response = self.socket.recv(self.config.BufferSize)
        if should_print:
            logging.info("{} - Received data, {} bytes", self.socket_id, len(response))
            print(repr(response))
        if len(response) == 0:
            self._graceful_shutdown_handler("Remote connection closed")
        return response

    def _handle_demo(self):
        # Receive hello message
        self.receive_data()

        self._accept_dictionary()

        file = self._accept_file()
        if file is not None:
            DataService.save_file(self.config.SaveFile, file)

    def _chat_loop(self):
        """
        Supports reading simple chat messages from the client
        """
        while self.is_connected:
            self.receive_data()

    def _accept_dictionary(self):
        """
        Deserializes a dictionary and attempts to read a python datetime object inside it.
        """
        received_dict = self.receive_data()
        deserialized_dict = DataService.deserialize(received_dict, self.config.DictionarySerializationMethod)
        logging.info("{} - Deserialized dict ({}):", self.socket_id, type(deserialized_dict))
        pprint.pprint(deserialized_dict, indent=2)
        logging.info("{} - Deserialized dict property of 'client-time': {}, type: {}",
                     self.socket_id, deserialized_dict['local_time'], type(deserialized_dict['local_time']))

    def _accept_file(self):
        """
        Expects a magic command from client that will tell us about the upcoming file's content length
        Then immediately afterwards expects a file.
        Optionally if configured decrypts the file.
        """
        if self.config.SaveFile is None:
            return None

        logging.info("Waiting for a file to accept")
        received_command: bytes = self._receive_data_unencrypted(should_print=False)
        is_file_command = received_command.startswith(self.config.FileCommand)
        if not is_file_command:
            raise CsckException("Received malformed magic command")

        expected_content_length, remaining_file_content = self._read_magic_command(received_command)
        logging.info("Will receive a file of content length {} bytes", expected_content_length)
        received_file = self._receive_file_to_end(remaining_file_content, expected_content_length)
        received_file = self._decrypt_file(received_file)
        logging.info("Accepted {} bytes, saving to {}", len(received_file), self.config.SaveFile)
        return received_file

    def _read_magic_command(self, received):
        """
        Reads a magic message from the client the upcoming file's content length

        Format:

        Custom-GUID-Bytes
        \n\n
        content length as unsigned big endian integer
        \n\n
        Custom-GUID-Bytes

        :param received: Data received from the socket. Possibly will contain magic message and some part of a file
        """
        file_cmd = self.config.FileCommand
        double_new_line = b'\n\n'

        payload = bytearray(received.removeprefix(file_cmd + double_new_line))
        ending_cmd_index = payload.index(double_new_line + file_cmd, 1)
        content_length_bytes = payload[0:ending_cmd_index]
        content_length = int.from_bytes(content_length_bytes, 'big', signed=False)
        file_starts_at = ending_cmd_index + len(file_cmd) + len(double_new_line)
        remaining_file_content = payload[file_starts_at:len(payload)]

        return content_length, remaining_file_content

    def _decrypt_file(self, received_file):
        """
        Decrypts a file if configured, otherwise does nothing
        """
        if self.config.EncryptionType == EncryptionType.Age:
            logging.info("Decrypting received file...")
            decrypted_file = self.crypt_service.decrypt(received_file)
            logging.info("Content length before vs after decryption: {} vs {}", len(received_file), len(decrypted_file))
            received_file = decrypted_file
        return received_file

    def _receive_file_to_end(self, buffer, expected_content_length):
        """
        After the magic message was read, we probably already read some part of the file.
        Since we already know the upcoming file's content length in bytes, we can read
        the remaining amount of bytes and append it to the buffer that we have already received.

        :param buffer: File's content that was already received
        :param expected_content_length: Expected full file's byte size
        :return: Whole file as a byte array
        """
        file_contents = bytearray(buffer)
        while len(file_contents) < expected_content_length:
            new_content: bytes = self._receive_data_unencrypted(should_print=False)
            file_contents += new_content
        if len(file_contents) > expected_content_length:
            err = "Received too many bytes!"
            logging.error(err + " {} vs {}", len(file_contents), expected_content_length)
            raise CsckException
        return file_contents

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
