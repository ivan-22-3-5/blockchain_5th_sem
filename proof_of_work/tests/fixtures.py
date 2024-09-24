import pytest

from src.block import Block
from src.transaction import Transaction


@pytest.fixture()
def make_transactions():
    def _inner(*, quantity):
        return [Transaction(recipient=f"recipient {i}", sender=f"sender {i}", amount=(i*i+5), fee=i*0.07) for i in range(quantity)]
    yield _inner


@pytest.fixture()
def block(make_transactions):
    transactions = make_transactions(quantity=7)
    yield Block(protocol_version="1.0",
                transactions=transactions,
                previous_hash="f21345",
                target="000",
                nonce=0)
