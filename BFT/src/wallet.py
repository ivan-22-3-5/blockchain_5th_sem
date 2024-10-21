from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey, generate_private_key
from cryptography.hazmat.primitives import serialization


class Wallet:
    def __init__(self, private_key: RSAPrivateKey = None, public_key: RSAPublicKey = None, address: str = None):
        self.private_key: RSAPrivateKey = generate_private_key(public_exponent=65537,
                                                               key_size=2048) if private_key is None else private_key
        self.public_key: RSAPublicKey = self.private_key.public_key() if public_key is None else public_key

    def to_dict(self):
        return {"private_key": self.private_key.private_bytes(serialization.Encoding.PEM,
                                                              serialization.PrivateFormat.PKCS8,
                                                              serialization.NoEncryption()).hex(),
                "public_key": self.public_key.public_bytes(serialization.Encoding.PEM,
                                                           serialization.PublicFormat.SubjectPublicKeyInfo).hex(),
                }
