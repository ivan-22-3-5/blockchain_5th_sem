import os
from time import sleep

from src.custom_exceptions import InsufficientFundsError
from src.node import Node


def main():
    node = Node(os.getenv("HOST", "127.0.0.1"), int(os.getenv("PORT", 5000)))
    node.start_mining()

    for _ in range(5):
        try:
            node.send_money("AnotherWallet", 10)
        except InsufficientFundsError:
            print("Failed to send transaction, not enough funds")
        sleep(15)


if __name__ == '__main__':
    main()
