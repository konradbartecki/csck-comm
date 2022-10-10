from cryptography.fernet import Fernet

from crypt_service import CryptService
from dictionary import some_dict
import json
import socket


def encrypt_data(py_object: object):
    '''
    This function generates a key, reads the previously created
    encrypted_file.txt, encodes the data with UTF-8, and then 
    encrypts the data and saves it locally
    '''
    output_file_encrypt = open('encrypted_file.txt', 'w')
    json.dump(py_object, output_file_encrypt)
    output_file_encrypt.close()
    
    print('We\'re all done!')

    # generate a key
    key = Fernet.generate_key()

    #save the key locally
    with open("my_key.key", "wb") as key_data:
        key_data.write(key)

    with open("encrypted_file.txt", "r") as outfile:
        data = outfile.read()

    # Converts the data into bytes because the encrypt funtion
    # needs byte encoded data
    read_text_file = data.encode()
    encrypted_text = CryptService().encrypt(read_text_file)

    with open('encrypted_file.txt', 'wb') as file:
        file.write(encrypted_text)

    file_contents: bytes
    with open('encrypted_file.txt', 'rb') as file:
        file_contents = file.read()

    print('File Encrypted!')
    print(file_contents)
    return file_contents
