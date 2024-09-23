from abc import ABC, abstractmethod
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


class Signable(ABC):
    def __init__(self):
        self.signature: Optional[str] = None

    def verify(self, key: RSAPublicKey) -> bool:
        if self.signature is None:
            return False
        try:
            key.verify(self.signature.encode(),
                       self.hash.encode(),
                       padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                           salt_length=padding.PSS.MAX_LENGTH),
                       algorithm=hashes.SHA256())
        except InvalidSignature:
            return False

    def sign(self, key: RSAPrivateKey):
        self.signature = key.sign(self.hash.encode(),
                                  padding=padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                      salt_length=padding.PSS.MAX_LENGTH),
                                  algorithm=hashes.SHA256()).decode()

    @property
    @abstractmethod
    def hash(self) -> str:
        ...
