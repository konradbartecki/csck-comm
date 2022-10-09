import unittest
from dictionary import some_dict
import sys
import socket
sys.path.insert(0, '')
from pickling import *


class TestPickling(unittest.TestCase):
    '''
    Class defining TestPickling
    '''
    # def test_encrypt_or_not_yes_choice(self):

    #     actual = encrypt_data(some_dict)
    #     expected = 'File Encrypted!'
    #     self.assertEqual(actual, expected)

    
    def test_encrpyt_or_not_no_choice(self):
        '''
        Tests if the function returns a serialised result from 
        dont_encrypt as that fucntion if the user chooses no
        '''
        actual = dont_encrypt(some_dict)
        expected = '{"name": "Betelgeuse", "type": "M1-2", "distance": "~600 ly", "constellation": "Orion"}'
        self.assertEqual(actual, expected)


    # def test_encrypt_or_not_incorrect_input(self):
    #     encrypt = 'x'
    #     actual = 
    #     expected = 'Please enter y or n'
    #     if encrypt in ['y', 'n']:
    #         return
    #     else:
    #         print('Please enter y or n')
    #     self.assertEqual(actual, expected)

    def test_dont_encrypt_json_pickling(self):
        '''
        Tests if the pickling choice returns a json type
        '''
        pickling_type = 'json'
        if pickling_type == 'json':
            data_str = str(json.dumps(some_dict))
        actual = data_str
        expected = '{"name": "Betelgeuse", "type": "M1-2", "distance": "~600 ly", "constellation": "Orion"}'
        self.assertEqual(actual, expected)

    def test_dont_encrypt_xml_pickling(self):
        '''
        Tests is the the pickling choice returns an xml type
        '''
        pickling_type = 'xml'
        if pickling_type == 'xml':
            data_str = dict2xml(some_dict)
        actual = data_str
        print(data_str)
        expected = 'b\'<constellation>Orion</constellation>\n<distance>~600 ly</distance>\n<name>Betelgeuse</name>\n<type>M1-2</type>'
        self.assertEqual(actual, expected)
    
    def test_dont_encrypt_xml_pickling(self):
        '''
        Tests is the the pickling choice returns an xml type
        '''
        pickling_type = 'binary'
        if pickling_type == 'binary':
            data_str = str(pickle.dumps(some_dict))
        actual = data_str
        expected = 'b\'\\x80\\x04\\x95T\\x00\\x00\\x00\\x00\\x00\\x00\\x00}\\x94(\\x8c\\x04name\\x94\\x8c\\nBetelgeuse\\x94\\x8c\\x04type\\x94\\x8c\\x04M1-2\\x94\\x8c\\x08distance\\x94\\x8c\\x07~600 ly\\x94\\x8c\\rconstellation\\x94\\x8c\\x05Orion\\x94u.'
        self.assertEqual(actual, expected)

    
class TestSocketClient(unittest.TestCase):
    '''
    Class defining SocketClient
    '''
    def test_client_program(self):
        '''
        Tests if the data has been succesfully encrypted
        '''

class TestSocketServer(unittest.TestCase):
    '''
    Class defining SocketServer
    '''
    def test_client_program(self):
        '''
        Tests if the data has been succesfully encrypted
        '''
        # Start game server in a background thread
    