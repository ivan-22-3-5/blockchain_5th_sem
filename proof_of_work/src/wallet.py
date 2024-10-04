from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey, generate_private_key

from src.utils import get_wallet_address


class Wallet:
    def __init__(self):
        self.private_key: RSAPrivateKey = generate_private_key(public_exponent=65537,
                                                               key_size=2048)
        self.public_key: RSAPublicKey = self.private_key.public_key()

        self.address: str = get_wallet_address(self.public_key)

