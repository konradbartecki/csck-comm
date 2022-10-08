from cryptography.fernet import Fernet

import socket

def encrypt_data(outfile):
    '''
    This function generates a key, reads the previouly created
    encrypted_file.txt, encodes the data with UTF-8, and then 
    encrypts the data and saves it locally
    '''
#generate a key
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

    
    
def send_encrypted_file(en_file):
    '''
    This function sends an encrypted file to the server 
    '''
    from cryptography.fernet import Fernet

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    BUFFER_SIZE = 4096
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server 

    with open('encrypted_file.txt', "r") as outfile:
        data = outfile.read(1024)
    byte_data = data.encode()

    
    key = Fernet.generate_key()
    ff = Fernet(key)
    
    enc = ff.encrypt(byte_data)
    client_socket.send(enc)
    print('Sent ', repr(enc))

    outfile.close()
    print('Encrypted File Sent!')

    client_socket.close


