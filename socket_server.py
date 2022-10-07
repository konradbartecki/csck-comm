import socket
import pickle
import json 
import xml.etree.ElementTree as ET

def server_program():

    host = socket.gethostname()
    port = 5000 

    server_socket = socket.socket()  

    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept() 
    print("Connection from: " + str(address))

    data = conn.recv(4096)

    # Using try/except to check if the data from the client
    # is of a certain type i.e. binary, json, or xml. If the
    # data enters the try clause and does not have the correct 
    # data type, it moves onto the next try clause until the can be loaded
    try:
        # binary data
        data_var = pickle.loads(data)
        print(data_var)
    except:
        try:
            # json data
            data_json = json.loads(data)
            print(data_json)
        except:
            try:
                # xml data
                print(data)
                tree = ET.parse(data)
                root = tree.getroot()
                print(root)
            except:
                print('not found')


    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()