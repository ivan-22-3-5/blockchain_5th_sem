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
    except (InvalidSignature, ValueError):
        return False
    return True


def sign(data: str, key: RSAPrivateKey) -> str:
    signature = key.sign(data.encode(),
                         padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                             salt_length=padding.PSS.MAX_LENGTH),
                         algorithm=hashes.SHA256())
    return signature.hex()
