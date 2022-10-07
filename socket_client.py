import socket
from pickling import dont_encrypt
from dictionary import some_dict
import os.path

def client_program():
    
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    BUFFER_SIZE = 4096
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server 

    # The dictionary is added as the argument for the sendall fuction
    # where dont_encrypt(some_dict) returns the serialised file to 
    # send to the server 
    client_socket.sendall(bytes(dont_encrypt(some_dict), encoding="utf-8"))

    client_socket.close()  # close the connection




if __name__ == '__main__':
    client_program()