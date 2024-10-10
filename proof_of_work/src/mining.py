from multiprocessing import Queue

from src.block import Block
from src.transaction import Transaction
from src.wallet import Wallet


def mine_block(transactions: list[dict], previous_hash: str, target: int, wallet: dict, *, queue: Queue):
    wallet = Wallet.from_dict(wallet)
    coin_base_wallet = Wallet()
    transactions = [Transaction(sender=coin_base_wallet.address, recipient=wallet.address, amount=50.0, fee=0).
                    sign(coin_base_wallet.private_key, coin_base_wallet.public_key),
                    Transaction(sender=coin_base_wallet.address, recipient=wallet.address, amount=50.0, fee=0).
                    sign(coin_base_wallet.private_key, coin_base_wallet.public_key),
                    *(Transaction.from_dict(t) for t in transactions)]
    for nonce in range(1_000_000_000):
        block = Block(transactions=transactions,
                      previous_hash=previous_hash,
                      target=target,
                      nonce=nonce).sign(wallet.private_key, wallet.public_key)
        if block.hash.startswith("0" * target):
            queue.put(block.to_dict())
            break
