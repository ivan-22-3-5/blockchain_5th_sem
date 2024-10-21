import time
from functools import wraps

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


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
