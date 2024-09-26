import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
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
    return private_key, public_key
