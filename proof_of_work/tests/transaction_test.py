from src.transaction import Transaction
from tests.fixtures import keys


def test_transaction_creation(keys):
    private_key, public_key = keys
    transaction = Transaction(sender=public_key, recipient=public_key, amount=100.0, fee=1.0)

    assert transaction.sender == public_key
    assert transaction.recipient == public_key
    assert transaction.amount == 100.0
    assert transaction.fee == 1.0
    assert transaction.signature is None
    assert transaction.timestamp is not None


def test_transaction_signing(keys):
    private_key, public_key = keys
    transaction = Transaction(sender=public_key, recipient=public_key, amount=100.0, fee=1.0)

    transaction.sign(private_key)

    assert transaction.signature is not None
    assert transaction.verify() is True


def test_transaction_verification_invalid_signature(keys):
    private_key, public_key = keys
    transaction = Transaction(sender=public_key, recipient=public_key, amount=100.0, fee=1.0)

    transaction.sign(private_key)

    transaction.signature = "invalid_signature"
    assert transaction.verify() is False
