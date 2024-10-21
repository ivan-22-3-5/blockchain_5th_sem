from src.block import Block
from src.transaction import Transaction


class Chain:
    def __init__(self):
        transactions = [Transaction(sender="qwerty123",
                                    recipient="qwerty123",
                                    amount=0,
                                    fee=0),
                        Transaction(sender="qwerty123",
                                    recipient="qwerty123",
                                    amount=0,
                                    fee=0)]
        self._chain: list[Block] = [Block(protocol_version="1.0",
                                          transactions=transactions,
                                          previous_hash="none")]

    def add_block(self, block: Block) -> bool:
        if not self.verify_block(block):
            return False
        print(f"Block {block.hash} added")
        self._chain.append(block)
        return True

    def verify_block(self, block: Block) -> bool:
        return all([
            block.verify(),
            block.previous_hash == self.last_block.hash,
        ])

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    def get_block_by_hash(self, target_hash: str) -> Block:
        for block in self._chain:
            if block.hash == target_hash:
                return block

    @property
    def last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]
