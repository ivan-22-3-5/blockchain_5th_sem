import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from src.block import Block
from src.chain import Chain
from src.transaction_pool import TransactionPool
from src.wallet import Wallet


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


@pytest.fixture()
def sender_and_recipient():
    yield Wallet(), Wallet()


@pytest.fixture
def keys():
    private_key, public_key = generate_keys()
    yield private_key, public_key


@pytest.fixture
def transactions(sender_and_recipient):
    transaction_pool = TransactionPool()
    sender, recipient = sender_and_recipient
    for i in range(10):
        sender.send_money(recipient.public_key, i)
    yield transaction_pool.get_transactions()


@pytest.fixture
def chain():
    yield Chain()


@pytest.fixture
def block(chain, transactions):
    block = Block(protocol_version="1.0",
                  transactions=transactions, previous_hash=chain.get_last_block().hash,
                  target=0, nonce=0)
    yield block
