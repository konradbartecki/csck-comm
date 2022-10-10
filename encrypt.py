from cryptography.fernet import Fernet
from dictionary import some_dict
import json
import socket

def encrypt_data(outfile):
    '''
    This function generates a key, reads the previouly created
    encrypted_file.txt, encodes the data with UTF-8, and then 
    encrypts the data and saves it locally
    '''
    output_file_encrypt = open('encrypted_file.txt', 'w')
    json.dump(some_dict, output_file_encrypt)
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
    byte_data = data.encode()

    f = Fernet(key)    

    encrypt_dict = f.encrypt(byte_data)
    
    with open('encrypted_file.txt', 'wb') as file:
        file.write(encrypt_dict)

    print('File Encrypted!')

    print(encrypt_dict)

    return str(encrypt_dict)
