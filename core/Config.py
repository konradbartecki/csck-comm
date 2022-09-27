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
    Mode: Mode
    TransferDataType: DataType
    WorkingDirectory: str
    # TODO: Encryption


@dataclass
class ClientConfig(Config):
    TargetAddress: str
    TargetPort: str


@dataclass
class ServerConfig(Config):
    ListenAddress: str
    ListenPort: str
