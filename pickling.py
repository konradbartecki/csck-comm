import pickle
import json
from dictionary import some_dict
from dict2xml import dict2xml
from encrypt import encrypt_data

def pickling_file_type(dict):
    '''
    This function prompts the user to encrypt their data,
    if not, the user is asked which format they want to pickle.
    If  the user encrypts their data, they asked if they want
    a copy of an uncrypted pickle file 
    '''
    pickling_formats = ['binary', 'json', 'xml']

    # While loop to ensure the user enteres the correct value 
    while True:
        encrypt = input('Will you be encrypting your data today?: ')
        if encrypt in ['y', 'n']:
            break
        else:
            print('Please enter y or n')
        continue


    def do_encrypt(dictionary):
        '''
        This function takes creates 'encrypted_file.txt' with
        the contents of the dictionary. Then calls the encrypt_data()
        function.
        The user is then asked if they would like an unencrypted
        pickle file. I f anything other than 'y' or 'n' is entered,
        the user is re-prompted
        '''
        output_file = open('encrypted_file.txt', 'w')
        json.dump(dictionary, output_file)
        output_file.close()
        encrypt_data(output_file)
        print('Done!')

        # While loop to ensure the user enteres the correct value 
        while True:
            keep_non_encypted = input('Would you like a copy of the non-encrypted pickle?: ')
            if keep_non_encypted in ['n', 'y']:
                break
            else:
                print('Please enter either y or n')
                continue
        if keep_non_encypted == 'y':
            dont_encrypt(dictionary)


    def dont_encrypt(dictionary):
        '''
        Asks the user what pickle type to use, if anything other than
        'n' or 'y' is entered, the user re-prompted. 
        Various statements are used to check the user input and
        create a corresponding pickle file
        '''
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
            output_file = open('json_dict.json', 'w')
            json.dump(dictionary, output_file)
            output_file.close()

        # Pickle's to binary
        if pickling_type == 'binary':
            output_file = open('bin_dict.bin', 'wb')
            pickle.dump(dictionary, output_file)
            output_file.close()
        
        # Pickles to xml
        if pickling_type == 'xml':
            xml = dict2xml(dictionary)
            output_file = open('xml_dict', 'w')
            output_file.write(xml)
            output_file.close()
        print('Done!')


    # Checks if the user wants to encrypt their file
    if encrypt == 'y':
        do_encrypt(dict)
    else:
        dont_encrypt(dict)


pickling_file_type(some_dict)
