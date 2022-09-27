# import relevant modules
import socket

# Variables in capital letters are constants such as PORT and SERVER

# We don't know size of msg received, so we use default 64 byte length
HEADER = 64

# Use a free port
PORT = 5050

# Enter decoding format below
FORMAT = 'utf-8'

# Message for client to disconnect from server
DISCONNECT_MESSAGE = "DISCONNECT SERVER"

# Enter local IP address. Clients must be connected to this IP to connect to the server
SERVER = '127.0.0.1'

ADDR = (SERVER, PORT)

# Code for the client to connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Function for sending messages to the server in an encoded format
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Pad message out so it matches the HEADER length in server (64 byte in this case)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # Using large message size "2048" as a large number so we can receive most unknown size messages.
    # This may need to be altered
    print(client.recv(2048).decode(FORMAT))
    
# Enter the message you would like to send below. Send DISCONNECT_MESSAGE to disconnect from the server.
# Example is sending a string
# For this project we need to serialise a dictionary and send it to the server. We also need to send text files fo server
# Adding serialision functions e.g pickle, will be soon be added to this project.


send("Hello, this is a test")
send(DISCONNECT_MESSAGE)

    