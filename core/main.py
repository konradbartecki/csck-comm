import sys
import socket
import argparse


from app_config import Mode, DataType, AppConfig
from csck_exceptions import CsckException
from client import Client
from server import Server


def prepare_argument_parser():
    parser = argparse.ArgumentParser(
        description='CSCK-COMM v1, simple TCP/IP communication tool with encryption support.')

    parser.add_argument('-m', '--mode', help='Sets the mode in which this app should operate', required=True,
                        choices=["Server", "Client"], type=str)
    parser.add_argument('-b', '--buffer', help='Buffer size in bytes', default=4096, type=int)
    parser.add_argument('-p', '--port', help='Port to use', default=5123, type=int)
    parser.add_argument('-ip', '--ip', help='IP Address to bind, '
                                            'as a server use 0.0.0.0 to bind on all available interfaces', type=str)
    parser.add_argument('-e', '--encoding', help='Text encoding to use', default="utf-8", type=str)
    parser.add_argument('-s', '--secure', help='Encryption method to use', type=str)
    parser.add_argument('-d', '--data', help='Data type that will be transferred', default="PlainText",
                        choices=["PlainText", "XML", "JSON", "Binary"], type=str)
    parser.add_argument('-f', '--file', nargs='?', help='File path to send or save to', type=argparse.FileType('r'),
                        default=sys.stdin)
    return parser

def prepare_config(args):
    mode = Mode[args.mode]
    port = int(args.port)
    ipaddress = str(args.ip)
    buffer_size = int(args.buffer)
    data_type = DataType[args.data]
    text_encoding = args.encoding
    file = args.file
    # TODO: Encryption
    return AppConfig(port, ipaddress, buffer_size, text_encoding, mode, data_type)


#Global config var
CONFIG:AppConfig

def main():
    parser = prepare_argument_parser()
    args = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()
        exit(1)
    CONFIG = prepare_config(args)
    new_socket = socket.socket()
    try:
        if CONFIG.Mode == Mode.Client:
            Client(CONFIG, new_socket).start()
        if CONFIG.Mode == Mode.Server:
            Server(CONFIG, new_socket).start()
    except(Exception) as e:
        print("General error!")
        socket.close()
    except(CsckException) as e:
        print("CSCK error!")
        socket.close()
    finally:
        print("init done")
    input("press close to exit")

main()