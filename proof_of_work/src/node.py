import base58

from src.block import Block
from src.chain import Chain
from src.transaction import Transaction
from src.transaction_pool import TransactionPool
from src.utils import ripemd160
from src.wallet import Wallet


class Node:
    def __init__(self):
        self.blockchain: Chain = Chain()
        self.transaction_pool: TransactionPool = TransactionPool()
        self.wallet: Wallet = Wallet()

    def mine_block(self, target: int) -> Block:
        coin_base_address = base58.b58encode(ripemd160('0')).decode()
        transactions = [Transaction(sender=coin_base_address, recipient=self.wallet.address, amount=50.0, fee=0),
                        Transaction(sender=coin_base_address, recipient=self.wallet.address, amount=50.0, fee=0),
                        *self.transaction_pool.get_transactions()]
        last_block_hash = self.blockchain.get_last_block().hash
        for nonce in range(1_000_000_000):
            block = Block(transactions=transactions,
                          previous_hash=last_block_hash,
                          target=target,
                          nonce=nonce).sign(self.wallet.private_key, self.wallet.public_key)
            if block.hash.startswith("0" * target):
                return block

    def send_money(self, recipient: str, amount: float):
        balance = self.blockchain.get_balance(self.wallet.address)
        if balance < amount:
            raise Exception("Insufficient funds")
        new_transaction = Transaction(self.wallet.address, recipient, amount, fee=amount * 0.01)
        self.transaction_pool.add(new_transaction.sign(self.wallet.private_key, self.wallet.public_key))
