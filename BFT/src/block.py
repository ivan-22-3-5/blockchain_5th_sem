from hashlib import sha256
from typing import Optional, Self

from pendulum import DateTime
from pendulum.tz import UTC
from merkly.mtree import MerkleTree
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization

from src.transaction import Transaction
from src.utils import verify_signature, sign


class Block:
    def __init__(self,
                 transactions: list[Transaction],
                 previous_hash: str,
                 timestamp: DateTime = DateTime.now(UTC),
                 merkle_root: str = None,
                 protocol_version: str = "1.0",
                 signature: str = None,
                 minter_public_key: RSAPublicKey = None,
                 hash: str = None):
        self.protocol_version: str = protocol_version
        self.timestamp: DateTime = timestamp
        self.transactions: list[Transaction] = transactions
        self.merkle_root: str = MerkleTree(
            [str(t) for t in self.transactions]).root.hex() if merkle_root is None else merkle_root
        self.previous_hash: str = previous_hash
        self.signature: Optional[str] = signature
        self.minter_public_key: Optional[RSAPublicKey] = minter_public_key
        self.hash: Optional[str] = hash

    def verify(self) -> bool:
        return all([
            MerkleTree([str(t) for t in self.transactions]).root.hex() == self.merkle_root,
            all(map(lambda t: t.verify(), self.transactions)),
            verify_signature(self.signature, self._signable_str(), self.minter_public_key),
            self.hash == sha256(str(self._hashable_str()).encode()).hexdigest()
        ])

    def sign(self, private_key: RSAPrivateKey, public_key: RSAPublicKey) -> Self:
        if self.signature is None:
            self.signature = sign(self._signable_str(), private_key)
            self.minter_public_key = public_key
            self.hash = sha256(str(self._hashable_str()).encode()).hexdigest()
        return self

    def to_dict(self, exclude: list[str] = None) -> dict:
        dict_repr = {
            "protocol_version": self.protocol_version,
            "timestamp": self.timestamp.for_json(),
            "merkle_root": self.merkle_root,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "signature": self.signature,
            "minter_public_key": self.minter_public_key.public_bytes(serialization.Encoding.PEM,
                                                                     serialization.PublicFormat.SubjectPublicKeyInfo).hex() if self.minter_public_key else None,
            "hash": self.hash
        }
        return {k: v for k, v in dict_repr.items() if k not in exclude} if exclude else dict_repr

    def _signable_str(self):
        return str(self.to_dict(exclude=["signature", "minter_public_key", "hash"]))

    def _hashable_str(self):
        return str(self.to_dict(exclude=["hash"]))

    def __str__(self):
        return str(self.to_dict())
