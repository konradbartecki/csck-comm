from pyrage import encrypt, decrypt, x25519


class CryptService:
    """
    Public-private key cryptography service
    Uses `age` as a backend and pre-generated public and private key
    """
    def __init__(self):
        self._private_key: str = x25519.Identity.from_str(open("assets/age_key", "r").read())
        self.public_key = x25519.Recipient.from_str(open("assets/age_key_pub", "r").read())

    def encrypt(self, b):
        return encrypt(bytes(b), [self.public_key])

    def decrypt(self, b):
        return decrypt(bytes(b), [self._private_key])