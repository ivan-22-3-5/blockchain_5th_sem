from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from src.block import Block


class Chain:
    def __init__(self):
        self._chain: list[Block] = [Block(protocol_version="1.0",
                                          transactions=[],
                                          previous_hash="none",
                                          target="none",
                                          nonce=0)]

    def add_block(self, miner_public_key: RSAPublicKey, block: Block):
        if block.verify(miner_public_key):
            self._chain.append(block)

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    def get_last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]
