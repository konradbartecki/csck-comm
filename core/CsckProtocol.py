from CsckExceptions import CsckMessageInvalidException
from strenum import StrEnum


class CsckProtocol:
    Version = "v1"
    HandshakeLine = f"CSCK-COMM/{Version} POST"


class CsckHeaders(StrEnum):
    ContentType = "Content-Type"
    ContentLength = "Content-Length"
    ContentEncoding = "Content-Encoding"
    EncryptionMode = "Encryption-Mode"


class CsckContentType(StrEnum):
    XML = "application/xml"
    JSON = "application/json"
    Binary = "binary"
    PlainText = "plain-text"


class CsckContentEncodings(StrEnum):
    UTF8 = "utf-8"
    UTF16 = "utf-16"


class CsckEncryptionMode(StrEnum):
    NoEncryption = "None"
    Fernet = "Fernet"
    Age = "Age"


class CsckMessage:
    def __init__(self, content: bytearray, headers: dict):
        CsckMessage.__validate_header_dictionary(headers)
        self._headers = headers
        self._content = content


    @staticmethod
    def __validate_header_dictionary(headers: dict):
        errors = []

        x = str(CsckHeaders.ContentEncoding)
        e = str(CsckContentEncodings.UTF8)

        for key in CsckHeaders:
            if headers.get(key) is None:
                errors.append(f"Header {key} is missing")

        # content_length = headers.get(CsckHeaders.ContentLength)
        content_type = headers.get(CsckHeaders.ContentType)
        content_encoding = headers.get(CsckHeaders.ContentEncoding)
        content_encryption = headers.get(CsckHeaders.EncryptionMode)

        # if content_length is not None and int(content_length) <= 0:
        #     errors.append(f"Value of {CsckHeaders.ContentLength} is invalid: {content_length}")

        if content_type is not None and CsckContentType(content_type) is None:
            errors.append(f"Value of {CsckHeaders.ContentType} is invalid: {content_type}"
                          f"Supported content types: {[', '.join(CsckContentType)]}")

        if content_encoding is not None and CsckContentEncodings(content_encoding) is None:
            errors.append(f"Value of {CsckHeaders.ContentEncoding} is not a supported encoding: {content_encoding}"
                          f"Supported encodings: {[', '.join(CsckContentEncodings)]}")

        if content_encryption is not None and CsckEncryptionMode(content_encryption) is None:
            errors.append(f"Value of {CsckHeaders.ContentEncoding} is invalid: {content_encoding}"
                          f"Supported encryption methods: {[', '.join(CsckEncryptionMode)]}")

        if len(errors) > 0:
            message = "This it not a valid CsckProtocol message, following errors were found:\n" + "\n".join(errors)
            raise CsckMessageInvalidException(message, errors)

    # def get_content_length(self):
    #     return int(self._headers[CsckHeaders.ContentLength])


