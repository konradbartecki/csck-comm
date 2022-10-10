import socket
import pickle
import json
import xml.etree.ElementTree as ET

import xmltodict

from crypt_service import CryptService


def server_program():
    host = socket.gethostname()
    port = 5111
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    data = conn.recv(4096)

    should_save_to_file = input('Should print data or safe to file? p/f (default=p)').lower() == 'f'
    is_encrypted = input("Is your content encrypted? y/n (default=n)").lower() == 'y'
    should_print = not should_save_to_file

    if is_encrypted:
        print("Decrypting data!")
        print(data)
        data = CryptService().decrypt(data)
        print("Decrypted into:")
        print(data)

    deserialized_data = deserialize_data(data, is_encrypted)
    if should_print:
        print_data(deserialized_data)
    else:
        save_data(data, "output_file.txt")
    conn.close()  # close the connection


def deserialize_data(data: bytes, should_decrypt):
    # Using try/except to check if the data from the client
    # is of a certain type i.e. binary, json, or xml. If the
    # dta enters the try clause and does not have the correct
    # data type, it moves onto the next try clause until it can be loaded
    pickling_formats = ['binary', 'json', 'xml']
    # While loop to ensure the user enteres the correct value
    pickling_type = 'json'
    if not should_decrypt:
        while True:
            pickling_type = input('Choose your pickling format: [xml, json, binary]').lower()
            if pickling_type in pickling_formats:
                break
            else:
                print('Incorrect format. Please enter binary, json, or xml')
                continue

    print("Will deserialize into %s" % pickling_type)
    print(data)
    if pickling_type == 'json':
        return json.loads(data)
    elif pickling_type == 'xml':
        decoded_str = data.decode('utf-8')
        return xmltodict.parse(decoded_str)['root']
    elif pickling_type == "binary":
        return pickle.loads(data)


def save_data(data:bytes, filename):
    open(filename, 'wb').write(data)
    print("Saved file to %s" % filename)


def print_data(str_data):
    print("Deserialized content:")
    print(str_data)


if __name__ == '__main__':
    server_program()
