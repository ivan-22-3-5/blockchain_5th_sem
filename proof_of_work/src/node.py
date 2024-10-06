import threading
import multiprocessing as mp
import json
import socket
import os

from block import Block
from chain import Chain
from mining import mine_block
from transaction import Transaction
from transaction_pool import TransactionPool
from wallet import Wallet


class Node:
    def __init__(self, host='127.0.0.1', port=5000):
        self.blockchain: Chain = Chain()
        self.transaction_pool: TransactionPool = TransactionPool()
        self.wallet: Wallet = Wallet()
        self.host = host
        self.port = port
        self.peers = []
        self.server = None
        self.mining_process: mp.Process = None
        self.is_mining = False
        self.initialize_connections()

    def initialize_connections(self):
        host_to_connect = os.getenv("HOST_TO_CONNECT", "")
        port_to_connect = int(os.getenv("PORT_TO_CONNECT", "0"))
        threading.Thread(target=self.start_server).start()
        if host_to_connect and port_to_connect:
            self.connect_to_peer(host_to_connect, port_to_connect)

    def start_mining(self):
        if self.is_mining:
            return
        threading.Thread(target=self._mine_block()).start()
        self.is_mining = True

    def stop_mining(self):
        if not self.is_mining:
            return
        self.is_mining = False
        self.mining_process.kill()

    def restart_mining(self):
        self.stop_mining()
        self.start_mining()

    def _mine_block(self):
        q = mp.Queue()
        self.mining_process = mp.Process(target=mine_block, args=(self.transaction_pool.get_transactions(),
                                                                  self.blockchain.get_last_block().hash,
                                                                  self.blockchain.current_target,
                                                                  self.wallet.to_dict()),
                                         kwargs={'queue': q})
        self.mining_process.start()
        self.blockchain.add_block(Block.from_dict(q.get()))
        print(f"Mined block: {self.blockchain.get_last_block().hash}")
        self.start_mining()
        self.mining_process.join()

    def send_money(self, recipient: str, amount: float):
        balance = self.blockchain.get_balance(self.wallet.address)
        if balance < amount:
            raise Exception("Insufficient funds")
        new_transaction = Transaction(self.wallet.address, recipient, amount, fee=amount * 0.01)
        self.transaction_pool.add(new_transaction.sign(self.wallet.private_key, self.wallet.public_key))

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Node is listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server.accept()
            self.peers.append(conn)
            print(f"Connected by {addr}")
            threading.Thread(target=self.handle_peer, args=(conn,)).start()

    def handle_peer(self, conn):
        try:
            self.peers.append(conn)
            while True:
                data = conn.recv(10240).decode()
                if not data:
                    break
                message = json.loads(data)
                self.process_message(message)
        except Exception as e:
            print(f"Error handling peer: {e}")

    def process_message(self, message):
        msg_type = message.get('type')
        match msg_type:
            case 'block':
                self.blockchain.add_block(Block.from_dict(message['block']))
            case 'transaction':
                self.transaction_pool.add(Transaction.from_dict(message['transaction']))
            case _:
                print(f"Unknown message type: {msg_type}")

    def connect_to_peer(self, peer_host, peer_port):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((peer_host, peer_port))
        self.peers.append(peer_socket)
        threading.Thread(target=self.listen_to_peer, args=(peer_socket,)).start()
        print(f"Connected to peer {peer_host}:{peer_port}")

    def listen_to_peer(self, peer_socket):
        try:
            while True:
                data = peer_socket.recv(10240).decode()
                if not data:
                    break
                message = json.loads(data)
                self.process_message(message)
        except Exception as e:
            print(f"Error in peer communication: {e}")

    def broadcast(self, message: dict):
        for peer in self.peers:
            try:
                peer.sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"Failed to send message to peer: {e}")

    def send_block(self, block: Block):
        print(f"Sending block: {block.hash}")
        message = {
            'type': 'block',
            'block': block.to_dict()
        }
        self.broadcast(message)

    def send_transaction(self, transaction: Transaction):
        message = {
            'type': 'transaction',
            'transaction': transaction.to_dict()
        }
        self.broadcast(message)
