from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    Client = 1
    Server = 2


class DataType(Enum):
    PlainText = 1
    XML = 2
    JSON = 3
    Binary = 4


@dataclass
class AppConfig:
    Mode: Mode = Mode.Client
    TransferDataType: DataType = DataType.Binary
    WorkingDirectory: str = "./tmp"
    # TODO: Encryption


@dataclass
class ClientAppConfig(AppConfig):
    def __init__(self):
        pass

    TargetAddress: str = "127.0.0.1"
    TargetPort: str = "9545"


@dataclass
class ServerAppConfig(AppConfig):
    def __init__(self):
        pass

    ListenAddress: str = "0.0.0.0"
    ListenPort: str = "9545"
