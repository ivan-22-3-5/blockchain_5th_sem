from hashlib import sha256
from typing import Optional, Self

from pendulum import DateTime
from pendulum.tz import UTC
from merkly.mtree import MerkleTree
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from src.transaction import Transaction
from src.utils import verify_signature, sign


class Block:
    def __init__(self, protocol_version: str, transactions: list[Transaction],
                 previous_hash: str, target: int, nonce: int = 0):
        self.protocol_version: str = protocol_version
        self.timestamp: DateTime = DateTime.now(UTC)
        self.transactions: list[Transaction] = transactions if transactions else None
        self.merkle_root: str = MerkleTree([str(t) for t in self.transactions]).root.hex() if transactions else None
        self.previous_hash: str = previous_hash
        self.target: int = target
        self.nonce: int = nonce
        self.signature: Optional[str] = None
        self.miner_public_key: Optional[RSAPublicKey] = None
        self.hash: Optional[str] = None

    def verify(self) -> bool:
        return all([
            MerkleTree([str(t) for t in self.transactions]).root.hex() == self.merkle_root,
            all(map(lambda t: t.verify(), self.transactions)),
            verify_signature(self.signature, self._signable_str(), self.miner_public_key),
            self.hash.startswith("0" * self.target),
            self.hash == sha256(str(self._hashable_str()).encode()).hexdigest()
        ])

    def sign(self, private_key: RSAPrivateKey, public_key: RSAPublicKey) -> Self:
        if self.signature is None:
            self.signature = sign(self._signable_str(), private_key)
            self.miner_public_key = public_key
            self.hash = sha256(str(self._hashable_str()).encode()).hexdigest()
        return self

    def to_dict(self, exclude: list[str] = None) -> dict:
        dict_repr = {
            "protocol_version": self.protocol_version,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "previous_hash": self.previous_hash,
            "target": self.target,
            "nonce": self.nonce,
            "signature": self.signature,
            "miner_public_key": self.miner_public_key,
            "hash": self.hash
        }
        return {k: v for k, v in dict_repr.items() if k not in exclude} if exclude else dict_repr

    def _signable_str(self):
        return str(self.to_dict(exclude=["signature", "miner_public_key", "hash"]))

    def _hashable_str(self):
        return str(self.to_dict(exclude=["hash"]))

    def __str__(self):
        return str(self.to_dict())
