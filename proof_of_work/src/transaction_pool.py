from src.transaction import Transaction
from src.utils import singleton


@singleton
class TransactionPool:
    def __init__(self):
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction):
        if transaction.verify():
            self._transactions.append(transaction)
