import pickle
import json

import dicttoxml

from crypt_service import CryptService
from dictionary import some_dict
from dict2xml import dict2xml
from encrypt import encrypt_data

save_or_not = True


def encrypt_or_not(py_object: object):
    '''
    Does the user want the data to be encrypted
    '''
    while True:
        encrypt = input('Are you encrypting the dictionary? y or n: ').lower()
        if encrypt in ['y', 'n']:
            break
        else:
            print('Please enter y or n')
        continue

    # Checks if the user wants to encrypt their file
    if encrypt == 'y':
        en_data = encrypt_data(py_object)
        return en_data
    else:
        data = dont_encrypt(py_object)

    return data


def dont_encrypt(py_object: object):
    '''
    Asks the user what pickle type to use, if anything other than
    'n' or 'y' is entered, the user re-prompted.
    Various statements are used to check the user input and
    create a corresponding pickle file
    '''

    pickling_formats = ['binary', 'json', 'xml']

    # While loop to ensure the user enteres the correct value
    while True:
        pickling_type = input('Choose your pickling format: ').lower()
        if pickling_type in pickling_formats:
            break
        else:
            print('Incorrect format. Please enter binary, json, or xml')
            continue

    # Pickle's to json
    if pickling_type == 'json':
        data_str = json.dumps(py_object)
        if save_or_not is True:
            output_file = open('json_dict.json', 'w')
            json.dump(py_object, output_file)
            output_file.close()

    # Pickle's to binary
    if pickling_type == 'binary':
        data_str = pickle.dumps(py_object)
        if save_or_not is True:
            output_file = open('bin_dict.bin', 'wb')
            pickle.dump(py_object, output_file)
            output_file.close()

    # Pickles to xml
    if pickling_type == 'xml':
        dicttoxml.set_debug(False)
        data_str: bytes = dicttoxml.dicttoxml(py_object, attr_type=False)
        if save_or_not is True:
            output_file = open('xml_dict', 'w')
            output_file.write(str(data_str))
            output_file.close()
    print('Pickled!')

    return data_str


if __name__ == '__main__':
    dont_encrypt(some_dict)
