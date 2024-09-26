from hashlib import sha256
from typing import Optional, Self

from pendulum import DateTime
from pendulum.tz import UTC
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from src.utils import verify_signature, sign


class Transaction:
    def __init__(self, sender: RSAPublicKey, recipient: RSAPublicKey, amount: float, fee: float):
        self.sender: RSAPublicKey = sender
        self.recipient: RSAPublicKey = recipient
        self.amount: float = amount
        self.fee: float = fee
        self.timestamp: DateTime = DateTime.now(UTC)
        self.signature: Optional[str] = None

    def verify(self) -> bool:
        return verify_signature(self.signature, self.hash, self.sender)

    def sign(self, private_key: RSAPrivateKey) -> Self:
        if self.signature is None:
            self.signature = sign(self.hash, private_key)
        return self

    @property
    def hash(self) -> str:
        return sha256(str(self.to_dict().update({"signature": None})).encode()).hexdigest()

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "signature": self.signature,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return str(self.to_dict())
