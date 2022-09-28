from cryptography.fernet import Fernet
from dictionary import some_dict


def encrypt_data(outfile):
    '''
    This function generates a key, reads the previouly created
    encrypted_file.txt, encodes the data with UTF-8, and then 
    encrypts the data
    '''
#generate a key
    key = Fernet.generate_key()

    #save the key locally
    with open("my_key.key", "wb") as key_data:
        key_data.write(key)

    with open("encrypted_file.txt", "r") as outfile:
        data = outfile.read()

    print(data)

    # Converts the data into bytes because the encrypt funtion
    # needs byte encoded data
    byte_data = data.encode()

    f = Fernet(key)    

    encrypt_dict = f.encrypt(byte_data)

    with open('encrypted_file.txt', 'wb') as file:
        file.write(encrypt_dict)

    print(encrypt_dict)

    return


