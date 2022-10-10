import socket
import pickle
import json
import xml.etree.ElementTree as ET

from cryptography.fernet import Fernet

from crypt_service import CryptService

print_data = True


def server_program():

    host = socket.gethostname()
    port = 5000
    should_encrypt = False

    server_socket = socket.socket()

    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    data = conn.recv(4096)

    str_data = str(data)

    if should_encrypt:
        print("Decrypting data!")
        print(str_data)
        str_data = CryptService().decrypt(str_data)
        print("Decrypted into:")
        print(str_data)
    if print_data:
        # Using try/except to check if the data from the client
        # is of a certain type i.e. binary, json, or xml. If the
        # dta enters the try clause and does not have the correct
        # data type, it moves onto the next try clause until it can be loaded
        try:
            # binary data
            data_var = pickle.loads(str_data)
            print(data_var)
        except:
            try:
                # json data
                data_json = json.loads(str_data)
                print(data_json)
            except:
                try:
                    # xml data
                    print(data)
                    tree = ET.parse(str_data)
                    root = tree.getroot()
                    print(root)
                except:
                    return
    # code = bytes(str_data, 'utf-8')
    # def call_key(): return open("my_key.key", "r").read()
    # key = call_key()
    # print(key)
    # f = Fernet(key)
    # print(f)
    # decoded_data = f.decrypt(code)
    # print(decoded_data)

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
