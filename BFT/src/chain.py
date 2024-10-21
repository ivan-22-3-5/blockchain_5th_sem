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
                                          previous_hash="none",
                                          target=0,
                                          nonce=0)]
        self.current_target: int = 4

    def add_block(self, block: Block) -> bool:
        if not self.verify_block(block):
            return False
        self._chain.append(block)
        print(f"Block {block.hash} added previous hash: {block.previous_hash}")
        if int(len(self._chain) / 1000) > self.current_target:
            self.current_target += 1
        return True

    def verify_block(self, block: Block) -> bool:
        return all([
            block.verify(),
            block.previous_hash == self.last_block.hash,
            self.current_target == block.target,
            self.last_block.timestamp < block.timestamp
        ])

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    @property
    def last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]
