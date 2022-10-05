# import relevant modules
import socket

# Default 64 byte length for incoming messages
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

# Bind client to the server
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
    # Print the message received confirmation being sent from the server
    print(client.recv(HEADER).decode(FORMAT))
    
# Enter the message you would like to send below. Send DISCONNECT_MESSAGE to disconnect from the server.
send(input('Enter your message here: '))

    