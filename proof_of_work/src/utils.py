from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


def verify_signature(signature: str, data: str, key: RSAPublicKey) -> bool:
    if signature is None:
        return False
    try:
        key.verify(signature.encode(),
                   data.encode(),
                   padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                       salt_length=padding.PSS.MAX_LENGTH),
                   algorithm=hashes.SHA256())
    except InvalidSignature:
        return False


def sign(data: str, key: RSAPrivateKey) -> str:
    return key.sign(data.encode(),
                    padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                        salt_length=padding.PSS.MAX_LENGTH),
                    algorithm=hashes.SHA256()).decode()
