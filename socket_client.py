import socket
from pickling import encrypt_or_not
from dictionary import some_dict


def client_program():

    encoding = 'utf-8'
    host = socket.gethostname()  # as both code is running on same pc
    port = 5111  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    # The dictionary is added as the argument for the sendall fuction
    # where dont_encrypt(some_dict) returns the serialised file to
    # send to the server
    converted_file = encrypt_or_not(some_dict)
    if type(converted_file) is str:
        converted_file = bytes(converted_file, encoding)
    client_socket.sendall(converted_file)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
