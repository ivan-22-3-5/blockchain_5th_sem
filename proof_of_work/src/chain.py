import base58

from src.block import Block
from src.transaction import Transaction
from src.utils import ripemd160


class Chain:
    def __init__(self):
        genesis_address = base58.b58encode(ripemd160('0')).decode()
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
        self.current_target: int = 4

    def add_block(self, block: Block):
        if self.verify_block(block):
            self._chain.append(block)
            if len(self._chain) % 1000 > self.current_target:
                self.current_target += 1

    def verify_block(self, block: Block) -> bool:
        return all([
            block.verify(),
            block.previous_hash == self.get_last_block().hash,
            self.current_target == block.target,
            self.get_last_block().timestamp < block.timestamp
        ])

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    def get_last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]

    def get_balance(self, address: str) -> float:
        balance: float = 0
        for block in self._chain:
            for transaction in block.transactions:
                if transaction.recipient == address:
                    balance += transaction.amount
                if transaction.sender == address:
                    balance -= transaction.amount + transaction.fee
        return balance
