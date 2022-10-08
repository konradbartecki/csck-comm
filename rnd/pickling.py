import pickle
import json
from assets.sample_dict import some_dict
from dict2xml import dict2xml
from encrypt import encrypt_data
from encrypt import send_encrypted_file

save_or_not = True

def do_encrypt(some_dict):
    '''
    This function takes creates 'encrypted_file.txt' with
    the contents of the dictionary. Then calls the encrypt_data()
    function.
    The user is then asked if they would like an unencrypted
    pickle file. I f anything other than 'y' or 'n' is entered,
    the user is re-prompted
    '''
    output_file_encrypt = open('encrypted_file.txt', 'w')
    json.dump(some_dict, output_file_encrypt)
    output_file_encrypt.close()
    encrypt_data(output_file_encrypt)
    print('We\'re all done!')

    while True:
        send_encrypted = input('Send encrypted file to the server? y or n: ')
        if send_encrypted in ['y', 'n']:
            break
        else:
            print('Please enter y or n')
    if send_encrypted == 'y':
        send_encrypted_file(some_dict)
        

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
        data_str = json.dumps(some_dict)
        if save_or_not == True:
            output_file = open('json_dict.json', 'w')
            json.dump(some_dict, output_file)
            output_file.close()

    # Pickle's to binary
    if pickling_type == 'binary':
        data_str = str(pickle.dumps(some_dict))
        if save_or_not == True:
            output_file = open('bin_dict.bin', 'wb')
            pickle.dump(some_dict, output_file)
            output_file.close()

    # Pickles to xml
    if pickling_type == 'xml':
        data_str = dict2xml(some_dict)
        if save_or_not == True:
            xml = dict2xml(some_dict)
            output_file = open('xml_dict', 'w')
            output_file.write(xml)
            output_file.close()
    print('Pickled!')

    while True:
        encrypt = input('Will you be encrypting your data today?: ')
        if encrypt in ['y', 'n']:
            break
        else:
            print('Please enter y or n')
        continue

    # Checks if the user wants to encrypt their file
    if encrypt == 'y':
        do_encrypt(some_dict)
    else:
        print('We\'re all done!')

    return data_str


if __name__ == '__main__':
    dont_encrypt(some_dict)