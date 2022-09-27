from dataclasses import dataclass


class Mode(enum):
    Client = 1
    Server = 2


class DataType(enum):
    PlainText = 1
    XML = 2
    JSON = 3
    Binary = 4


@dataclass
class Config:
    Mode: Mode = Mode.Client
    TransferDataType: DataType = DataType.Binary
    WorkingDirectory: str = "./tmp"
    # TODO: Encryption


@dataclass
class ClientConfig(Config):
    def __init__(self):
        pass

    TargetAddress: str = "127.0.0.1"
    TargetPort: str = "9545"


@dataclass
class ServerConfig(Config):
    def __init__(self):
        pass

    ListenAddress: str = "0.0.0.0"
    ListenPort: str = "9545"
