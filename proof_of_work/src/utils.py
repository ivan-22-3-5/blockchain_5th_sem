import hashlib

import base58
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def verify_signature(signature: str, data: str, key: RSAPublicKey) -> bool:
    if signature is None:
        return False
    try:
        key.verify(bytes.fromhex(signature),
                   data.encode(),
                   padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                       salt_length=padding.PSS.MAX_LENGTH),
                   algorithm=hashes.SHA256())
    except InvalidSignature:
        return False
    except ValueError:
        return False

    return True


def sign(data: str, key: RSAPrivateKey) -> str:
    signature = key.sign(data.encode(),
                         padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                             salt_length=padding.PSS.MAX_LENGTH),
                         algorithm=hashes.SHA256())
    return signature.hex()


def get_wallet_address(public_key: RSAPublicKey) -> str:
    return base58.b58encode(ripemd160(hashlib.sha256(str(public_key).encode()).hexdigest())).decode()


def ripemd160(data: str) -> bytes:
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(hashlib.sha256(data.encode()).digest())
    return ripemd160_hash.digest()
