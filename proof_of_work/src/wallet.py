from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey, generate_private_key


from src.transaction import Transaction
from src.transaction_pool import TransactionPool
from src.utils import get_wallet_address
from src.wallet_address import WalletAddress


class Wallet:
    def __init__(self):
        self.private_key: RSAPrivateKey = generate_private_key(public_exponent=65537,
                                                               key_size=2048)
        self.public_key: RSAPublicKey = self.private_key.public_key()

        self.address: WalletAddress = get_wallet_address(self.public_key)

    def send_money(self, recipient: WalletAddress, amount: float):
        new_transaction = Transaction(self.address,
                                      recipient,
                                      amount - amount * 0.01,
                                      fee=amount * 0.01)
        TransactionPool().add(new_transaction.sign(self.private_key, self.public_key))
