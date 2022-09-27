import socket
import threading
from config import Config

class Server:
    def __init__(self, config: Config):
        if config is None:
            raise ValueError("Config must be provided")
        self.config = config


    def start_accepting_connections(self):
        listening_address = (self.config.IPAddress, self.config.Port)
        current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            current_socket.bind(listening_address)
        except Exception as e:
            print("Exception thrown" + e)
            exit(-1)

        print("Server connection is being established...")
        current_socket.listen()
        print(f"Server is listening on IP address: {listening_address}")
        should_continue_listening = True
        while should_continue_listening:
            (connection, address) = current_socket.accept()

            #TODO: Accept input from console
            #When "exit" is written then
            #Set 'should_continue_listening' to false

            thread = threading.Thread(target=handle_client, args=(connection, address))
            thread.start()
            print(f"[Live connections] {threading.activeCount() - 1}")

    def handle_client(conn, addr):
        print(f"[New connection] {addr} connected to server")

        # State how many bytes we want to receive from the client
        # Decode message from bytes format
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                # Print client address and message
                print(f"[{addr}] {msg}")
                # Confirm receipt of message by messaging client
                conn.send("Message received".encode(FORMAT))

        # Close connection
        conn.close()
