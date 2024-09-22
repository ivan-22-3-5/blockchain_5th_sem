from src.block import Block


class Blockchain:
    def __init__(self):
        self._chain: list[Block] = []

    def add_block(self, block: Block):
        if block.verify():
            self._chain.append(block)

    def get_block(self, index: int) -> Block:
        if 0 < index < len(self._chain):
            return self._chain[index]

    def get_last_block(self) -> Block:
        if len(self._chain) > 0:
            return self._chain[-1]
