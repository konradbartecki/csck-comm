from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    Client = 1
    Server = 2


class DataType(Enum):
    plain_text = 1
    xml = 2
    json = 3
    binary = 4


@dataclass
class Config:
    mode: Mode = Mode.Client
    data_type: DataType = DataType.binary
    working_directory: str = "./tmp"
    ip_address: str = ""
    port: int = ""
    # TODO: Encryption