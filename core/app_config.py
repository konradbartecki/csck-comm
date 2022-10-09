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
    XML = 1
    JSON = 2
    Binary = 3


@dataclass
class AppConfig:
    Port: int
    IPAddress: str
    BufferSize: int = 4096
    TextEncoding: str = "utf-8"
    Mode: Mode = Mode.Client,
    DictionarySerializationMethod: DataType = DataType.Binary
    EncryptionType: EncryptionType = EncryptionType.NoEncryption
    CloseMessage : bytes = b"36c6552c-4e8e-4415-8748-0d078598cd7b"
