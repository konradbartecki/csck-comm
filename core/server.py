import logging
import os
import signal
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor

from app_config import AppConfig
import socket

from server_connection_handler import ServerConnectionHandler


class Server:
    def __init__(self, config: AppConfig, server_socket: socket):
        self.listening_thread = None
        self.config = config
        self.server_socket = server_socket
        self.is_accepting = True
        self.threads = []

    def start(self):
        logging.info("Starting a listener at {}:{}", self.config.IPAddress, self.config.Port)
        self.server_socket.bind((self.config.IPAddress, self.config.Port))
        self.server_socket.listen()
        self.listening_thread = threading.Thread(target=self.listen)
        self.listening_thread.start()
        self._register_graceful_shutdown_handler()

    def listen(self):
        while self.is_accepting:
            logging.info("Waiting for a connection to accept")
            try:
                (conn, address) = self.server_socket.accept()
                logging.info('Connection from {}', address)
                connection_handler_thread = threading.Thread(target=ServerConnectionHandler(conn, self.config).handle)
                self.threads.append(connection_handler_thread)
                connection_handler_thread.start()
            except ConnectionAbortedError:
                logging.warning('Listener thread stopping...')
                self.is_accepting = False;
                return

    def _register_graceful_shutdown_handler(self):
        """
        Registers a handler for CTRL-C interrupt event
        """
        signal.signal(signal.SIGINT, self._graceful_shutdown_handler)

    def _graceful_shutdown_handler(self, signum, frame):
        logging.warning("Shutting down server listener gracefully by interrupt")
        self.is_accepting = False
        self.server_socket.close()
        exit(0)
