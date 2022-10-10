import socket
import pickle
import json
import xml.etree.ElementTree as ET

from cryptography.fernet import Fernet

from crypt_service import CryptService

print_data = True
should_decrypt = False


def server_program():

    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    data = conn.recv(4096)

    str_data = str(data)

    if should_decrypt:
        print("Decrypting data!")
        print(str_data)
        str_data = CryptService().decrypt(str_data)
        print("Decrypted into:")
        print(str_data)

    deserialized_data = deserialize_data(str_data)
    if print_data:
        print_data(deserialized_data)
    else:
        save_data(deserialized_data, "output_file.txt")
    conn.close()  # close the connection


def deserialize_data(str_data):
    # Using try/except to check if the data from the client
    # is of a certain type i.e. binary, json, or xml. If the
    # dta enters the try clause and does not have the correct
    # data type, it moves onto the next try clause until it can be loaded
    try:
        # binary data
        return  pickle.loads(str_data)
    except:
        try:
            # json data
            return json.loads(str_data)
        except:
            # xml data
            tree = ET.parse(str_data)
            return tree.getroot()


def save_data(str_data):
    open('output_file.txt', 'w').write(str_data)


def print_data(str_data):
    print(str_data)


if __name__ == '__main__':
    server_program()
