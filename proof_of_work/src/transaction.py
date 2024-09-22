from hashlib import sha256

from pendulum import DateTime
from pendulum.tz import UTC


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, fee: float, signature: str):
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: float = amount
        self.fee: float = fee
        self.signature: str = signature
        self.timestamp: DateTime = DateTime.now(UTC)

    @property
    def hash(self) -> str:
        return sha256(str(self).encode()).hexdigest()

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
