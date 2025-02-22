from hashlib import sha256
from typing import Optional, Self

from pendulum import DateTime
from pendulum.tz import UTC
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import serialization

from src.utils import verify_signature, sign


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, fee: float,
                 timestamp: DateTime = DateTime.now(UTC), signature: str = None,
                 sender_public_key: RSAPublicKey = None, hash: str = None):
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: float = amount
        self.fee: float = fee
        self.timestamp: DateTime = timestamp
        self.signature: Optional[str] = signature
        self.sender_public_key: Optional[RSAPublicKey] = sender_public_key
        self.hash: Optional[str] = hash

    def verify(self) -> bool:
        return all([
            verify_signature(self.signature, self._signable_str(), self.sender_public_key),
            self.hash == sha256(str(self._hashable_str()).encode()).hexdigest()
        ])

    def sign(self, private_key: RSAPrivateKey, public_key: RSAPublicKey) -> Self:
        if self.signature is None:
            self.signature = sign(self._signable_str(), private_key)
            self.sender_public_key = public_key
            self.hash = sha256(str(self._hashable_str()).encode()).hexdigest()
        return self

    def to_dict(self, exclude: list[str] = None):
        dict_repr = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "timestamp": self.timestamp.for_json(),
            "signature": self.signature,
            "sender_public_key": self.sender_public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo).hex() if self.sender_public_key else None,
            "hash": self.hash
        }
        return {k: v for k, v in dict_repr.items() if k not in exclude} if exclude else dict_repr

    def _signable_str(self):
        return str(self.to_dict(exclude=["signature", "sender_public_key", "hash"]))

    def _hashable_str(self):
        return str(self.to_dict(exclude=["hash"]))

    def __str__(self):
        return str(self.to_dict())
