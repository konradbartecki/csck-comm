import logging
import signal
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app_config import AppConfig
import socket

from server_connection_handler import ServerConnectionHandler


class Server:
    def __init__(self, config:AppConfig, server_socket:socket):
        self.config = config
        self.server_socket = server_socket
        self.is_accepting = True

    def start(self):
        logging.info("Starting a listener at {}:{}", self.config.IPAddress, self.config.Port)
        self.server_socket.bind((self.config.IPAddress, self.config.Port))
        self.server_socket.listen(10)
        with ThreadPoolExecutor() as e:
            self._register_graceful_shutdown_handler()
            #TODO: Shutdown this thread gracefully
            e.submit(self.listen(e))

    def listen(self, executor: ThreadPoolExecutor):
        while self.is_accepting:
            (conn, address) = self.server_socket.accept()
            with conn:
                executor.submit(self.handle_connection(conn, address))

    def handle_connection(self, conn, address):
        logging.info('Connection from {}', address)
        ServerConnectionHandler(conn, self.config).handle()

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
