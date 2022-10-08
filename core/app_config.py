from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    Client = 1
    Server = 2


class EncryptionType(Enum):
    NoEncryption = 1
    Fernet = 2
    Age = 3


class DataType(Enum):
    PlainText = 1
    XML = 2
    JSON = 3
    Binary = 4


@dataclass
class AppConfig:
    Port: int
    IPAddress: str
    BufferSize: int = 4096
    TextEncoding: str = "utf-8"
    Mode: Mode = Mode.Client,
    TransferDataType: DataType = DataType.Binary
    EncryptionType: EncryptionType = EncryptionType.NoEncryption
