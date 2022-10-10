import pickle
import json
from dictionary import some_dict
from dict2xml import dict2xml
from encrypt import encrypt_data

save_or_not = True


def encrypt_or_not(some_dict):
    '''
    Does the user want the data to be encrypted
    '''
    while True:
        encrypt = input('Are you encrypting the dictionary? y or n: ')
        if encrypt in ['y', 'n']:
            break
        else:
            print('Please enter y or n')
        continue

    # Checks if the user wants to encrypt their file
    if encrypt == 'y':
        en_data = encrypt_data(some_dict)
        return en_data
    else:
        data = dont_encrypt(some_dict)

    return data


def dont_encrypt(some_dict):
    '''
    Asks the user what pickle type to use, if anything other than
    'n' or 'y' is entered, the user re-prompted.
    Various statements are used to check the user input and
    create a corresponding pickle file
    '''

    pickling_formats = ['binary', 'json', 'xml']

    # While loop to ensure the user enteres the correct value
    while True:
        pickling_type = input('Choose your pickling format: ')
        if pickling_type in pickling_formats:
            break
        else:
            print('Incorrect format. Please enter binary, json, or xml')
            continue

    # Pickle's to json
    if pickling_type == 'json':
        data_str = str(json.dumps(some_dict))
        if save_or_not is True:
            output_file = open('json_dict.json', 'w')
            json.dump(some_dict, output_file)
            output_file.close()

    # Pickle's to binary
    if pickling_type == 'binary':
        data_str = str(pickle.dumps(some_dict))
        if save_or_not is True:
            output_file = open('bin_dict.bin', 'wb')
            pickle.dump(some_dict, output_file)
            output_file.close()

    # Pickles to xml
    if pickling_type == 'xml':
        data_str = dict2xml(some_dict)
        if save_or_not is True:
            xml = dict2xml(some_dict)
            output_file = open('xml_dict', 'w')
            output_file.write(xml)
            output_file.close()
    print('Pickled!')

    return data_str


if __name__ == '__main__':
    dont_encrypt(some_dict)
