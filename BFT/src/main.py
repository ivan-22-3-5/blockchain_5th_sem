from node import Node
from src.utils import timeit


@timeit
def start_process(node: Node):
    node.issue_block()


def main():
    n = 10
    nodes = [Node() for _ in range(n)]

    for i in range(n):
        for j in range(1, n):
            if i != j:
                nodes[i].connect_peer(nodes[j])

    start_process(nodes[0])


if __name__ == '__main__':
    main()
