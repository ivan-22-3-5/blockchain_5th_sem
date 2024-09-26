from hashlib import sha256
from typing import Optional, Self

from pendulum import DateTime
from pendulum.tz import UTC
from merkly.mtree import MerkleTree
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from src.transaction import Transaction
from src.utils import verify_signature, sign


class Block:
    def __init__(self, protocol_version: str, transactions: list[Transaction], previous_hash: str, target: str,
                 nonce: int = 0):
        self.protocol_version: str = protocol_version
        self.timestamp: DateTime = DateTime.now(UTC)
        self.transactions: MerkleTree = MerkleTree(list(map(lambda t: str(t), transactions)))
        self.merkle_root: str = self.transactions.root.decode("utf-8")
        self.previous_hash: str = previous_hash
        self.target: str = target
        self.nonce: int = nonce
        self.signature: Optional[str] = None

    def verify(self, miner_public_key: RSAPublicKey) -> bool:
        if MerkleTree(self.transactions.raw_leaves).root != self.merkle_root:
            return False
        return verify_signature(self.signature, self.hash, miner_public_key)

    def sign(self, private_key: RSAPrivateKey) -> Self:
        if self.signature is None:
            self.signature = sign(self.hash, private_key)
        return self

    @property
    def hash(self) -> str:
        return sha256(str(self).encode()).hexdigest()

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
