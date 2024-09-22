from hashlib import sha256

from pendulum import DateTime
from pendulum.tz import UTC
from merkly.mtree import MerkleTree

from src.transaction import Transaction


class Block:
    def __init__(self,
                 protocol_version: str, transactions: list[Transaction],
                 previous_hash: str, target: str, signature: str, nonce: int = 0):
        self.protocol_version: str = protocol_version
        self.timestamp: DateTime = DateTime.now(UTC)
        self.transactions: MerkleTree = MerkleTree(list(map(lambda t: t.__str__(), transactions)))
        self.merkle_root: str = self.transactions.root.decode("utf-8")
        self.previous_hash: str = previous_hash
        self.target: str = target
        self.nonce: int = nonce
        self.signature: str = signature

    @property
    def hash(self) -> str:
        return sha256(str(self).encode()).hexdigest()

    def verify(self) -> bool:
        ...

    def to_dict(self) -> dict:
        return {
            "protocol_version": self.protocol_version,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "target": self.target,
            "nonce": self.nonce,
            "signature": self.signature
        }

    def __str__(self):
        return self.to_dict().__str__()
