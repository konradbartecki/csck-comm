# Client/Server network - Group project

## Simple client-server communication app with encryption written in Python

The purpose of this project is to build a client/server network where a client can transmit Python objects to a server via TCP/IP protocol. This project includes the below features:

* Send a serialised dictionary from a client to the server.
* The dictionary can be set to the following pickling formats: Binary, JSON, XML.
* Send text file from a client to the server. The client has the option to encrypt this file.
* The server has a configurable option to print the contents of the received files.
* Unit tests to validate the code's functionality

## Installation and usage instructions

1. Clone this project into your IDE using the link https://github.com/konradbartecki/csck-comm
2. Install requirements.txt by using the following command: pip install -r requirements.txt
3. In your terminal, enter the command "python socket_server.py" to start listening for clients
4. In a seperate (or split) terminal, enter the command "python socket_client.py" to connect to the server and send objects

## Contributors
* Konrad Bartecki
* Jason Hadwen
* Phillip Gregory




