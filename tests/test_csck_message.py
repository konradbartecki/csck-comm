import unittest

from CsckExceptions import CsckMessageInvalidException
from CsckProtocol import CsckContentType, CsckContentEncodings, CsckEncryptionMode, CsckHeaders, CsckMessage


class CsckMessageTests(unittest.TestCase):
    def test_init_CsckMessage(self):
        content = bytearray([1, 2, 3])
        content_type = CsckContentType.Binary
        content_encoding = CsckContentEncodings.UTF8
        encryption = CsckEncryptionMode.NoEncryption

        headers = [
            [CsckHeaders.ContentType, content_type],
            [CsckHeaders.ContentEncoding, content_encoding],
            [CsckHeaders.ContentLength, len(content)],
            [CsckHeaders.EncryptionMode, encryption]
        ]

        CsckMessage(content, headers)

    def test_init_can_validate_unknown_content_type(self):
        content = bytearray([1, 2, 3])
        content_type = "image/jpeg"
        content_encoding = CsckContentEncodings.UTF8
        encryption = CsckEncryptionMode.NoEncryption

        headers = [
            [CsckHeaders.ContentType, content_type],
            [CsckHeaders.ContentEncoding, content_encoding],
            [CsckHeaders.ContentLength, len(content)],
            [CsckHeaders.EncryptionMode, encryption]
        ]

        with self.assertRaises(CsckMessageInvalidException):
            CsckMessage(content, headers)


if __name__ == '__main__':
    unittest.main()
