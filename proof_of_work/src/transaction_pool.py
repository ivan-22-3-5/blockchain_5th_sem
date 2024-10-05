from src.transaction import Transaction


class TransactionPool:
    def __init__(self):
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction):
        if transaction.verify():
            self._transactions.append(transaction)

    def get_transactions(self) -> list[Transaction]:
        return sorted(self._transactions, key=lambda t: t.fee, reverse=True)[:5]
