# import relevant modules. 
# Threading allows multiple clients to connect without a single client blocking the connection
import socket
import threading

# Variables in capital letters are constants such as PORT and SERVER

# We don't know size of msg received, so we use default 64 byte length
HEADER = 64

# Use a free port
PORT = 5050

# Code to automatically generate the IP address to run server on
SERVER = socket.gethostbyname(socket.gethostname())

# Address
ADDR = (SERVER, PORT)

# Enter decoding format below
FORMAT = 'utf-8'

# Message for client to disconnect from server
DISCONNECT_MESSAGE = "DISCONNECT SERVER"

# Create new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket
server.bind(ADDR)

# Create functions to connect client to server

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
        
    

# Listen for new connections and display how many clients are connected to the server
def start():
    server.listen()
    # Message to state which IP we are listening from
    print(f"Server is listening on IP address: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        thread.start()
        print(f"[Live connections] {threading.activeCount() -1}")

# Message to confirm server connection is live
print("Server connection is being established...")
start()
