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

    # try/except here because binary does not like being encoded 
    # and gives an error. So the first try clause takes the binary
    # file, while the second try clause takes json and xml 
    try:
        client_socket.sendall(bytes(dont_encrypt(some_dict)))
    except:
        try:
            client_socket.sendall(bytes(dont_encrypt(some_dict), encoding="utf-8"))
        except:
            return print('Check format. Probably trying to serialise a string')

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()