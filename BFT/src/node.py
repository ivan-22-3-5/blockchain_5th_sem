from time import sleep
from collections import defaultdict

from block import Block
from chain import Chain
from src.transaction import Transaction
from src.wallet import Wallet


class Node:
    def __init__(self):
        self.blockchain: Chain = Chain()
        self.wallet = Wallet()
        self.peers = []
        self.pending_blocks = {}
        self.block_confirmations = defaultdict(int)

    def receive_block(self, block: Block):
        if self.blockchain.verify_block(block):
            if self.block_confirmations[block.hash] >= len(self.peers) * 2 / 3:
                self.blockchain.add_block(block)
            else:
                if block.hash not in self.pending_blocks:
                    self.pending_blocks[block.hash] = block
            self.send_block_confirmation(block.hash)

    def receive_message(self, message: str):
        block_hash, validity = [s.strip() for s in message.split(':')]
        if self.blockchain.get_block_by_hash(block_hash):
            return
        if validity == 'valid':
            self.block_confirmations[block_hash] += 1
            if self.block_confirmations[block_hash] < len(self.peers) * 2 / 3:
                return
            if (block := self.pending_blocks.pop(block_hash, None)) is not None:
                self.blockchain.add_block(block)

    def connect_peer(self, peer: 'Node'):
        self.peers.append(peer)

    def broadcast_block(self, block: Block):
        for peer in self.peers:
            peer.receive_block(block)

    def send_block_confirmation(self, block_hash: str):
        for peer in self.peers:
            peer.receive_message(f"{block_hash}: valid")
            sleep(0.01)

    def issue_block(self):
        block = Block(
            transactions=[Transaction(
                sender="qwerty123",
                recipient="qwerty123",
                amount=1,
                fee=0
            ).sign(self.wallet.private_key, self.wallet.public_key), Transaction(
                sender="qwerty123",
                recipient="qwerty123",
                amount=1,
                fee=0
            ).sign(self.wallet.private_key, self.wallet.public_key)],
            previous_hash=self.blockchain.last_block.hash
        ).sign(self.wallet.private_key, self.wallet.public_key)

        self.blockchain.add_block(block)
        self.broadcast_block(block)
