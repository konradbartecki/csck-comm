import argparse
from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class Mode(Enum):
    Client = 1
    Server = 2


class EncryptionType(Enum):
    NoEncryption = 1
    Age = 2


class DataType(Enum):
    XML = 1
    JSON = 2
    Binary = 3


@dataclass
class AppConfig:
    Port: int
    IPAddress: str
    SaveFile : argparse.FileType
    ReadFile : argparse.FileType
    BufferSize: int = 4096
    TextEncoding: str = "utf-8"
    Mode: Mode = Mode.Client,
    DictionarySerializationMethod: DataType = DataType.Binary
    EncryptionType: EncryptionType = EncryptionType.NoEncryption
    FileCommand = UUID("f58bfeed-8c3e-4a4f-bae1-1138877dc457").bytes
