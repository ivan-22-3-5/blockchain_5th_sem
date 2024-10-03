from src.block import Block
from src.transaction import Transaction
from src.utils import ripemd160
from src.wallet_address import WalletAddress


class Chain:
    def __init__(self):
        genesis_address = WalletAddress(address_bytes=ripemd160('0'))
        transactions = [Transaction(sender=genesis_address,
                                    recipient=genesis_address,
                                    amount=0,
                                    fee=0),
                        Transaction(sender=genesis_address,
                                    recipient=genesis_address,
                                    amount=0,
                                    fee=0)]
        self._chain: list[Block] = [Block(protocol_version="1.0",
                                          transactions=transactions,
                                          previous_hash="none",
                                          target=0,
                                          nonce=0)]

    def add_block(self, block: Block):
        if block.verify() and self.get_last_block().timestamp < block.timestamp:
            self._chain.append(block)

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    def get_last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]
