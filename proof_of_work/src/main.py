import os
from time import sleep

from src.node import Node


def main():
    node = Node(os.getenv("HOST", "127.0.0.1"), int(os.getenv("PORT", 5000)))
    node.start_mining()

    while True:
        sleep(10)


if __name__ == '__main__':
    main()
