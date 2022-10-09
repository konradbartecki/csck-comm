import sys
import socket
import argparse

from app_config import Mode, DataType, AppConfig
from client import Client
from color_formatter import ColorizedArgsFormatter
from csck_exceptions import CsckException
import logging

from server import Server


def init_logging():
    console_format = "%(levelname)s %(asctime)s - %(message)s"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    colored_formatter = ColorizedArgsFormatter(console_format)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)


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
    parser.add_argument('-i', '--interactive', help='Interactive client to server chat mode', type=str)
    parser.add_argument('-dsm', '--serialization-method',
                        choices=["Binary", "XML", "JSON"],
                        help='Data type that will be used for de/serialization for a dictionary',
                        default="JSON", type=str)
    parser.add_argument('-f', '--file', nargs='?',
                        help='File path to send or save to', type=argparse.FileType('r'),
                        default=sys.stdin)
    return parser


def prepare_config(args):
    mode = Mode[args.mode]
    port = int(args.port)
    ipaddress = str(args.ip)
    buffer_size = int(args.buffer)
    data_type = DataType[args.serialization_method]
    text_encoding = args.encoding
    # file = args.file
    # TODO: Encryption
    return AppConfig(port, ipaddress, buffer_size, text_encoding, mode, data_type)


def client_loop(config, new_socket):
    c = Client(config, new_socket)
    c.start()
    while True:
        msg = input("Send message below or CTRL-C to exit:\n")
        if msg == "exit":
            c.close()
        else:
            c.send_text(msg)


def main():
    init_logging()
    logging.info("CSCK-COMM v1, press {} to exit", "CTRL-C")
    parser = prepare_argument_parser()
    args = parser.parse_args()
    has_no_arguments_provided = len(sys.argv) <= 1
    if has_no_arguments_provided:
        parser.print_help()
        exit(1)

    config = prepare_config(args)
    new_socket = socket.socket()
    logging.info("{}", config.Mode)
    try:
        if config.Mode == Mode.Client:
            client_loop(config, new_socket)
        if config.Mode == Mode.Server:
            Server(config, new_socket).start()
    except CsckException as e:
        logging.error("CSCK error! \n{}", repr(e))
        raise e
    except Exception as e:
        logging.error("General error! \n{}", repr(e))
        raise e


main()
