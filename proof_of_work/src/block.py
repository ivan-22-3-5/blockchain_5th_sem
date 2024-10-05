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
                 target: int,
                 nonce: int,
                 timestamp: DateTime = DateTime.now(UTC),
                 merkle_root: str = None,
                 protocol_version: str = "1.0",
                 signature: str = None,
                 miner_public_key: RSAPublicKey = None,
                 hash: str = None):
        self.protocol_version: str = protocol_version
        self.timestamp: DateTime = timestamp
        self.transactions: list[Transaction] = transactions
        self.merkle_root: str = MerkleTree(
            [str(t) for t in self.transactions]).root.hex() if merkle_root is None else merkle_root
        self.previous_hash: str = previous_hash
        self.target: int = target
        self.nonce: int = nonce
        self.signature: Optional[str] = signature
        self.miner_public_key: Optional[RSAPublicKey] = miner_public_key
        self.hash: Optional[str] = hash

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
            "timestamp": self.timestamp.for_json(),
            "merkle_root": self.merkle_root,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "target": self.target,
            "nonce": self.nonce,
            "signature": self.signature,
            "miner_public_key": self.miner_public_key.public_bytes(serialization.Encoding.PEM,
                                                                   serialization.PublicFormat.SubjectPublicKeyInfo).hex() if self.miner_public_key else None,
            "hash": self.hash
        }
        return {k: v for k, v in dict_repr.items() if k not in exclude} if exclude else dict_repr

    @staticmethod
    def from_dict(dict_repr: dict) -> 'Block':
        return Block(
            protocol_version=dict_repr["protocol_version"],
            timestamp=DateTime.fromisoformat(dict_repr["timestamp"]),
            merkle_root=dict_repr["merkle_root"],
            transactions=[Transaction.from_dict(t) for t in dict_repr["transactions"]],
            previous_hash=dict_repr["previous_hash"],
            target=dict_repr["target"],
            nonce=dict_repr["nonce"],
            signature=dict_repr["signature"],
            miner_public_key=serialization.load_pem_public_key(bytes.fromhex(dict_repr["miner_public_key"])),
            hash=dict_repr["hash"]
        )

    def _signable_str(self):
        return str(self.to_dict(exclude=["signature", "miner_public_key", "hash"]))

    def _hashable_str(self):
        return str(self.to_dict(exclude=["hash"]))

    def __str__(self):
        return str(self.to_dict())
